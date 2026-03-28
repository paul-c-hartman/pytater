#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-or-later

# All built in modules.
import os
import sys
import tempfile
import time

# This package's modules.
from nerd_dictation.config import settings
from nerd_dictation.utilities import *
from nerd_dictation.post_processors import process_text
from nerd_dictation.vosk import text_from_vosk_pipe
from nerd_dictation.simulate_input import input_fns

# Types.
from typing import Optional
from types import ModuleType

# -----------------------------------------------------------------------------
# Custom Configuration
#
# TODO: we aren't touching this section because we're going to tear it up and
# replace it with setuptools entry points. not pulling this out to its own
# module

def user_config_as_module_or_none(
    config_override: Optional[str],
    user_config_prev: Optional[ModuleType],
) -> Optional[ModuleType]:
    # Explicitly ask for no configuration.
    if config_override == "":
        return None
    if config_override is None:
        user_config_path = os.path.join(settings.dirs.user_config_path, "nerd-dictation.py")
        if not os.path.exists(user_config_path):
            return None
    else:
        user_config_path = config_override
        # Allow the exception for a custom configuration.

    try:
        user_config = execfile(user_config_path)
    except Exception as ex:
        sys.stderr.write('Failed to run "{:s}" with error: {:s}\n'.format(user_config_path, str(ex)))
        if user_config_prev is not None:
            # Reloading configuration at run-time, don't exit in this case - use the previous config instead.
            sys.stderr.write("Reload failed, continuing with previous configuration.\n")
            user_config = user_config_prev
        else:
            # Exit if the user starts with an invalid configuration.
            sys.exit(1)

    return user_config

def main_begin(
    *,
    vosk_model_dir: str,
    path_to_cookie: str = "",
    pulse_device_name: str = "",
    sample_rate: int = 44100,
    input_method: str = "PAREC",
    progressive: bool = False,
    progressive_continuous: bool = False,
    full_sentence: bool = False,
    numbers_as_digits: bool = False,
    numbers_use_separator: bool = False,
    numbers_min_value: Optional[int] = None,
    numbers_no_suffix: bool = False,
    timeout: float = 0.0,
    idle_time: float = 0.0,
    delay_exit: float = 0.0,
    punctuate_from_previous_timeout: float = 0.0,
    config_override: Optional[str],
    output: str = "TYPE",
    simulate_input_tool: str = "XDOTOOL",
    suspend_on_start: bool = False,
    verbose: int = 0,
    vosk_grammar_file: str = "",
) -> None:
    """
    Initialize audio recording, then full text to speech conversion can take place.

    This is terminated by the ``end`` or ``cancel`` actions.
    """

    # Find language model in:
    # - `--vosk-model-dir=...`
    # - `~/.config/nerd-dictation/model`
    if not vosk_model_dir:
        vosk_model_dir = os.path.join(settings.dirs.user_data_path, "model")
        # If this still doesn't exist the error is handled later.

    #
    # Initialize the recording state and perform some sanity checks.
    #
    if not path_to_cookie:
        path_to_cookie = os.path.join(tempfile.gettempdir(), settings.temp_cookie_name)

    is_run_on = False
    if punctuate_from_previous_timeout > 0.0:
        age_in_seconds: Optional[float] = None
        try:
            age_in_seconds = file_age_in_seconds(path_to_cookie)
        except FileNotFoundError:
            age_in_seconds = None
        is_run_on = age_in_seconds is not None and (age_in_seconds < punctuate_from_previous_timeout)
        del age_in_seconds

    # Write the PID, needed for suspend/resume sub-commands to know the PID of the current process.
    with open(path_to_cookie, "w", encoding="utf-8") as fh:
        fh.write(str(os.getpid()))

    # Force zero time-stamp so a fast begin/end (tap) action
    # doesn't leave dictation running.
    touch(path_to_cookie, mtime=0)
    cookie_timestamp = file_mtime_or_none(path_to_cookie)
    if cookie_timestamp != 0:
        sys.stderr.write("Cookie removed after right after creation (unlikely but respect the request)\n")
        return

    #
    # Start recording the output file.
    #

    touch_mtime = None
    use_overtime = delay_exit > 0.0 and timeout == 0.0

    # Lazy loaded so recording can start 1st.
    user_config = None

    def exit_fn(handled_any: bool) -> int:
        nonlocal touch_mtime
        if not os.path.exists(path_to_cookie):
            return -1  # Cancel.
        if file_mtime_or_none(path_to_cookie) != cookie_timestamp:
            # Only delay exit if some text has been handled,
            # this prevents accidental tapping of push to talk from running.
            if handled_any:
                # Implement `delay_exit` workaround.
                if use_overtime:
                    if touch_mtime is None:
                        touch_mtime = time.time()
                    if time.time() - touch_mtime < delay_exit:
                        # Continue until `delay_exit` is reached.
                        return 0
                # End `delay_exit`.

            return 1  # End.
        return 0  # Continue.

    process_fn_is_first = True

    def process_fn(text: str) -> str:
        nonlocal process_fn_is_first

        if not text:
            return ""

        #
        # Simple text post processing and capitalization.
        #
        config = {
            "full_sentence": {"enabled": full_sentence},
            "numbers": {
                "enabled": True,
                "as_digits": numbers_as_digits,
                "use_separator": numbers_use_separator,
                "min_value": numbers_min_value,
                "no_suffix": numbers_no_suffix,
            },
        }
        text = process_text(text, config)

        if is_run_on:
            # This is a signal that the end of the sentence has been reached.
            if full_sentence:
                text = ". " + text
            else:
                text = ", " + text

        process_fn_is_first = False

        return text

    #
    # Handled the resulting text
    #
    if output == "SIMULATE_INPUT":
        handle_fn = input_fns.get(simulate_input_tool)
        if handle_fn is None:
            raise Exception("Internal error, unknown input tool: {!r}".format(simulate_input_tool))

    else:
        # Unreachable.
        assert False

    found_any = text_from_vosk_pipe(
        vosk_model_dir=vosk_model_dir,
        pulse_device_name=pulse_device_name,
        sample_rate=sample_rate,
        input_method=input_method,
        timeout=timeout,
        idle_time=idle_time,
        progressive=progressive,
        progressive_continuous=progressive_continuous,
        exit_fn=exit_fn,
        process_fn=process_fn,
        handle_fn=handle_fn,
        suspend_on_start=suspend_on_start,
        verbose=verbose,
        vosk_grammar_file=vosk_grammar_file,
    )

    if not found_any:
        sys.stderr.write("No text found in the audio\n")
        # Avoid continuing punctuation from where this recording (which recorded nothing) left off.
        touch(path_to_cookie)
        return

def main_end(
    *,
    path_to_cookie: str = "",
) -> None:
    if not path_to_cookie:
        path_to_cookie = os.path.join(tempfile.gettempdir(), settings.temp_cookie_name)

    # Resume (does nothing if not suspended), so suspending doesn't prevent the cancel operation.
    main_suspend(path_to_cookie=path_to_cookie, suspend=False, verbose=0)

    touch(path_to_cookie)

def main_cancel(
    *,
    path_to_cookie: str = "",
) -> None:
    if not path_to_cookie:
        path_to_cookie = os.path.join(tempfile.gettempdir(), settings.temp_cookie_name)

    # Resume (does nothing if not suspended), so suspending doesn't prevent the cancel operation.
    main_suspend(path_to_cookie=path_to_cookie, suspend=False, verbose=0)

    file_remove_if_exists(path_to_cookie)

def main_suspend(
    *,
    path_to_cookie: str = "",
    suspend: bool,
    verbose: int,
) -> None:
    import signal

    if not path_to_cookie:
        path_to_cookie = os.path.join(tempfile.gettempdir(), settings.temp_cookie_name)

    if not os.path.exists(path_to_cookie):
        if verbose >= 1:
            sys.stderr.write("No running nerd-dictation cookie found at: {:s}, abort!\n".format(path_to_cookie))
        return

    with open(path_to_cookie, "r", encoding="utf-8") as fh:
        data = fh.read()
    try:
        pid = int(data)
    except Exception as ex:
        if verbose >= 1:
            sys.stderr.write("Failed to read PID with error {!r}, abort!\n".format(ex))
        return

    if suspend:
        os.kill(pid, signal.SIGUSR1)
    else:  # Resume.
        os.kill(pid, signal.SIGCONT)
