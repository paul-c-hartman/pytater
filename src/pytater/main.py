"""This is the main module for the pytater application.

It contains the main functions that are called when the user runs the application. This includes the main entry points for starting, ending, and canceling the speech recognition process, as well as handling the suspend and resume functionality.
"""

# All built in modules.
import os
import tempfile
import time

# Types.
from typing import Optional

# This package's modules.
from pytater.config import settings
from pytater.utilities import touch, file_mtime_or_none, file_age_in_seconds, file_remove_if_exists
from pytater.post_processors import process_text
from pytater.vosk import text_from_vosk_pipe
from pytater.simulate_input import input_fns
from pytater.logging import logger


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
    output: str = "TYPE",
    simulate_input_tool: str = "XDOTOOL",
    suspend_on_start: bool = False,
    vosk_grammar_file: str = "",
) -> None:
    """Initialize audio recording so that full text-to-speech conversion can take place.

    This is terminated by the `end` or `cancel` actions.

    Args:
        vosk_model_dir: The directory containing the VOSK model to use for speech recognition.
        path_to_cookie: The path to the cookie file used for managing the recording state. If empty, a default path will be used.
        pulse_device_name: The name of the PulseAudio device to use for recording. If empty, the default device will be used.
        sample_rate: The sample rate to use for recording audio.
        input_method: The method to use for capturing audio input. Supported values are "PAREC", "SOX", and "PW-CAT".
        progressive: Whether to enable progressive transcription, which outputs text as it is recognized rather than waiting for the end of the sentence.
        progressive_continuous: Whether to enable continuous progressive transcription, which continues to output text as it is recognized even after the end of the sentence is reached.
        full_sentence: Whether to treat the recognized text as a full sentence, which affects punctuation and capitalization.
        numbers_as_digits: Whether to convert recognized numbers to digits (e.g., "twenty" to "20").
        numbers_use_separator: Whether to use a separator (e.g., a comma) when converting recognized numbers to digits.
        numbers_min_value: The minimum value for converting recognized numbers to digits. If None, there is no minimum.
        numbers_no_suffix: Whether to avoid adding a suffix (e.g., "th") when converting recognized numbers to digits.
        timeout: The maximum time in seconds to wait for speech input before timing out. If 0, there is no timeout.
        idle_time: The time in seconds to wait for additional speech input after the end of a sentence is detected before finalizing the transcription. If 0, there is no idle time.
        delay_exit: The time in seconds to delay the exit after the end of a sentence is detected. This can be used to allow for additional speech input to be included in the transcription. If 0, there is no delay.
        punctuate_from_previous_timeout: The time in seconds to consider the previous transcription as part of the current sentence for punctuation purposes. This can be used to continue punctuation from the previous transcription if the user is speaking in short bursts. If 0, there is no continuation from the previous transcription.
        output: The method to use for outputting the transcribed text. Supported values are "SIMULATE_INPUT" for using a specified input simulation tool.
        simulate_input_tool: The tool to use for simulating input when `output` is set to "SIMULATE_INPUT".
        suspend_on_start: Whether to suspend the recording process immediately after starting, allowing it to be resumed later.
        vosk_grammar_file: The path to a VOSK grammar file to use for constraining the speech recognition. If empty, no grammar will be used.

    Raises:
        RuntimeError: If an unknown input method or output method is specified, or if the specified input simulation tool is unknown. These are considered internal errors that should never happen under normal usage (i.e., when using the `pytater` command-line tool). You may run into these errors if you are using the Python API directly; if you are not, please report the bug on this project's issues page.
    """

    # Find language model in:
    # - `--vosk-model-dir=...`
    # - `~/.config/pytater/model`
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
        logger.warning("Cookie removed after right after creation (unlikely but respect the request)\n")
        return

    #
    # Start recording the output file.
    #

    touch_mtime = None
    use_overtime = delay_exit > 0.0 and timeout == 0.0

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
            raise RuntimeError(f"Internal error, unknown input tool: {simulate_input_tool!r}")

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
        vosk_grammar_file=vosk_grammar_file,
    )

    if not found_any:
        logger.debug("No text found in the audio\n")
        # Avoid continuing punctuation from where this recording (which recorded nothing) left off.
        touch(path_to_cookie)
        return


def main_end(
    *,
    path_to_cookie: str = "",
) -> None:
    """End the recording process, finalizing any remaining tasks.

    Args:
        path_to_cookie: The path to the cookie file used for managing the recording state. If empty, a default path will be used.
    """
    if not path_to_cookie:
        path_to_cookie = os.path.join(tempfile.gettempdir(), settings.temp_cookie_name)

    # Resume (does nothing if not suspended), so suspending doesn't prevent the cancel operation.
    main_suspend(path_to_cookie=path_to_cookie, suspend=False)

    touch(path_to_cookie)


def main_cancel(
    *,
    path_to_cookie: str = "",
) -> None:
    """Cancel the recording process, discarding any transcribed text.

    Args:
        path_to_cookie: The path to the cookie file used for managing the recording state. If empty, a default path will be used.
    """
    if not path_to_cookie:
        path_to_cookie = os.path.join(tempfile.gettempdir(), settings.temp_cookie_name)

    # Resume (does nothing if not suspended), so suspending doesn't prevent the cancel operation.
    main_suspend(path_to_cookie=path_to_cookie, suspend=False)

    file_remove_if_exists(path_to_cookie)


def main_suspend(
    *,
    path_to_cookie: str = "",
    suspend: bool,
) -> None:
    """Suspend or resume the recording process.

    Args:
        path_to_cookie: The path to the cookie file used for managing the recording state. If empty, a default path will be used.
        suspend: Whether to suspend (True) or resume (False) the recording process.
    """
    import signal

    if not path_to_cookie:
        path_to_cookie = os.path.join(tempfile.gettempdir(), settings.temp_cookie_name)

    if not os.path.exists(path_to_cookie):
        logger.info("No running pytater cookie found at: %s, abort!\n", str(path_to_cookie))
        return

    with open(path_to_cookie, "r", encoding="utf-8") as fh:
        data = fh.read()
    try:
        pid = int(data)
    except Exception as ex:
        logger.info("Failed to read PID with error %s, abort!\n", str(ex))
        return

    if suspend:
        os.kill(pid, signal.SIGUSR1)
    else:  # Resume.
        os.kill(pid, signal.SIGCONT)
