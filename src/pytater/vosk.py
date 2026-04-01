"""This module facilitates speech recognition using the VOSK library.

It hooks into the VOSK speech recognition library to provide real-time transcription of audio input.

Typical usage example:

    from pytater.vosk import text_from_vosk_pipe
    text_from_vosk_pipe(
        vosk_model_dir="path/to/model",
        exit_fn=your_exit_fn,
        process_fn=your_process_fn,
        handle_fn=your_handle_fn,
        timeout=5.0,
        idle_time=0.1,
        progressive=True,
        progressive_continuous=False,
        sample_rate=44100,
        input_method="PAREC",
        pulse_device_name="",
        suspend_on_start=False,
        verbose=0,
        vosk_grammar_file="",
    )
"""

import os
import subprocess
import sys
import time
from typing import IO, Tuple, Callable, List, Optional
from pytater.utilities import file_handle_make_non_blocking
from pytater.config import settings


def recording_proc_with_non_blocking_stdout(
    input_method: str,
    sample_rate: int,
    pulse_device_name: str,
    # NOTE: typed as a string for Py3.6 compatibility.
) -> "Tuple[subprocess.Popen[bytes], IO[bytes]]":
    if input_method == "PAREC":
        cmd = (
            "parec",
            "--record",
            f"--rate={sample_rate}",
            "--channels=1",
            *((f"--device={pulse_device_name}",) if pulse_device_name else ()),
            "--format=s16ne",
            "--latency=10",
        )
    elif input_method == "SOX":
        cmd = (
            "sox",
            "-q",
            "-V1",
            "-d",
            "--buffer",
            "1000",
            "-r",
            f"{sample_rate}",
            "-b",
            "16",
            "-e",
            "signed-integer",
            "-c",
            "1",
            "-t",
            "raw",
            "-L",
            "-",
        )
    elif input_method == "PW-CAT":
        cmd = (
            "pw-cat",
            "--record",
            "--format=s16",
            "--rate",
            f"{sample_rate}",
            "--channels=1",
            "-",
        )
    else:
        sys.stderr.write(f"--input {input_method!r} not supported.\n")
        sys.exit(1)

    ps = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    stdout = ps.stdout
    assert stdout is not None

    # Needed so whatever is available can be read (without waiting).
    file_handle_make_non_blocking(stdout)

    return ps, stdout


def text_from_vosk_pipe(
    *,
    vosk_model_dir: str,
    exit_fn: Callable[..., int],
    process_fn: Callable[[str], str],
    handle_fn: Callable[[int, str], None],
    timeout: float,
    idle_time: float,
    progressive: bool,
    progressive_continuous: bool,
    sample_rate: int,
    input_method: str,
    pulse_device_name: str = "",
    suspend_on_start: bool = False,
    verbose: int = 0,
    vosk_grammar_file: str = "",
) -> bool:
    """Runs the VOSK speech recognition process and handles the output according to the provided functions and parameters.
    
    This function is the core of the speech recognition process, handling the recording of audio, processing it with VOSK, and managing the output based on the provided callbacks and settings.

    Args:
        vosk_model_dir: The directory where the VOSK model is located.
        exit_fn: A callback function that determines when to exit the recording loop. It should return -1 to cancel, 0 to continue, and 1 to finish.
        process_fn: A callback function that processes the transcribed text before it is handled. It takes a string input and returns a string output.
        handle_fn: A callback function that handles the processed text. It takes an integer representing the number of characters to delete from the previous output and a string representing the new text to output.
        timeout: The time in seconds to wait for changes in the transcription before automatically exiting. A value of 0 means no timeout.
        idle_time: The time in seconds to sleep between iterations of the recording loop to prevent excessive CPU usage. A value of 0 means no sleeping.
        progressive: If True, the handle_fn will be called with partial results as they are transcribed. If False, handle_fn will only be called with the final transcribed text.
        progressive_continuous: If True and progressive is True, the handle_fn will be called with the continuously updated transcription. If False and progressive is True, the handle_fn will be called with the final transcription of each segment.
        sample_rate: The sample rate for audio recording.
        input_method: The method to use for audio input. Supported values are "PAREC", "SOX", and "PW-CAT".
        pulse_device_name: The name of the PulseAudio device to use for recording (only applicable if input_method is "PAREC").
        suspend_on_start: If True, the recording process will start in a suspended state and will need to be resumed with a signal (e.g., SIGCONT).
        verbose: The verbosity level for logging. Higher values will produce more detailed logs.
        vosk_grammar_file: The path to a file containing a JSON array of grammar rules for VOSK. If empty, no grammar will be used.
    
    Returns:
        A boolean indicating whether any text was handled during the recording process.
    """
    # Delay some imports until recording has started to avoid minor delays.
    import json

    if not os.path.exists(vosk_model_dir):
        sys.stderr.write(
            "Please download a model using `pytater download`.\n"
        )
        sys.exit(1)

    # NOTE: typed as a string for Py3.6 compatibility.
    def recording_proc_start() -> "Tuple[subprocess.Popen[bytes], IO[bytes]]":
        return recording_proc_with_non_blocking_stdout(input_method, sample_rate, pulse_device_name)

    has_ps = False
    if not suspend_on_start:
        ps, stdout = recording_proc_start()
        has_ps = True

    # `mypy` doesn't know about VOSK.
    import vosk  # type: ignore

    vosk.SetLogLevel(-1)

    if not vosk_grammar_file:
        grammar_json = ""
    else:
        with open(vosk_grammar_file, encoding="utf-8") as fh:
            grammar_json = fh.read()

    # Allow for loading the model to take some time:
    if verbose >= 1:
        sys.stderr.write("Loading model...\n")
    model = vosk.Model(vosk_model_dir)

    if grammar_json == "":
        rec = vosk.KaldiRecognizer(model, sample_rate)
    else:
        rec = vosk.KaldiRecognizer(model, sample_rate, grammar_json)

    if verbose >= 1:
        sys.stderr.write("Model loaded.\n")

    # 1mb
    block_size = 1_048_576

    use_timeout = timeout != 0.0
    if use_timeout:
        timeout_text_prev = ""
        timeout_time_prev = time.time()

    # Collect the output used when time-out is enabled.
    if not (progressive and progressive_continuous):
        text_list: List[str] = []

    # Set true if handle has been called.
    handled_any = False

    if progressive:
        text_prev = ""

    # Track this to prevent excessive load when the "partial" result doesn't change.
    json_text_partial_prev = ""

    # -----------------------------
    # Utilities for Text Processing

    def handle_fn_suspended() -> None:
        nonlocal handled_any
        nonlocal text_prev
        nonlocal json_text_partial_prev

        handled_any = False
        text_prev = ""
        json_text_partial_prev = ""

        if not (progressive and progressive_continuous):
            text_list.clear()

    def handle_fn_wrapper(text: str, is_partial_arg: bool) -> None:
        nonlocal handled_any
        nonlocal text_prev

        # Simple deferred text input, just accumulate values in a list (finish entering text on exit).
        if not progressive:
            if is_partial_arg:
                return
            text_list.append(text)
            handled_any = True
            return

        # Progressive support (type as you speak).
        if progressive_continuous:
            text_curr = process_fn(text)
        else:
            text_curr = process_fn(" ".join(text_list + [text]))

        if text_curr != text_prev:
            match = min(len(text_curr), len(text_prev))
            for i in range(min(len(text_curr), len(text_prev))):
                if text_curr[i] != text_prev[i]:
                    match = i
                    break

            # Emit text, deleting any previous incorrectly transcribed output
            handle_fn(len(text_prev) - match, text_curr[match:])

            text_prev = text_curr

        if not is_partial_arg:
            if progressive_continuous:
                text_prev = ""
            else:
                text_list.append(text)

        handled_any = True

    # -----------------------------------------------
    # Utilities for accessing results on `rec` (VOSK)

    def rec_handle_fn_wrapper_from_final_result() -> str:
        json_text = rec.FinalResult()

        # When `rec.FinalResult()` returns an empty string, typically immediately after a resume,
        # it can cause the JSON decoder to fail. This patch simply ignores that case and continues
        # by returning an empty string to the caller.
        if not json_text:
            return ""

        assert isinstance(json_text, str)
        json_data = json.loads(json_text)
        text = json_data["text"]
        assert isinstance(text, str)
        if text:
            handle_fn_wrapper(text, False)
        return json_text

    def rec_handle_fn_wrapper_from_partial_result(json_text_partial_prev: str) -> Tuple[str, str]:
        json_text = rec.PartialResult()
        # Without this, there are *many* calls with the same partial text.
        if json_text_partial_prev != json_text:
            json_text_partial_prev = json_text

            json_data = json.loads(json_text)
            # In rare cases this can be unset (when resuming from being suspended).
            text = json_data.get("partial", "")
            if text:
                handle_fn_wrapper(text, True)
        return json_text, json_text_partial_prev

    if not suspend_on_start:
        # Support setting up input simulation state.
        handle_fn(settings.simulate_input_code_command, "SETUP")

    # Use code to delay exiting, allowing reading the recording buffer to catch-up.
    code = 0

    # ---------------
    # Signal Handling

    suspend = suspend_on_start

    from types import FrameType

    def do_suspend_pause() -> None:
        nonlocal has_ps, ps, stdout
        rec_handle_fn_wrapper_from_final_result()

        # Don't include any of the current analysis when resuming.
        rec.Reset()

        # Clear the buffer:
        handle_fn_suspended()

        nonlocal verbose
        if verbose >= 1:
            sys.stderr.write("Recording suspended.\n")

        # Close the recording process.
        if has_ps:
            # Support setting up input simulation state.
            handle_fn(settings.simulate_input_code_command, "TEARDOWN")

            stdout.close()
            os.kill(ps.pid, signal.SIGINT)
            del stdout, ps
            has_ps = False

    # Warning: do not call do_suspend_resume() from a signal context because it
    # can cause reentrant runtime errors and other related bugs.
    def do_suspend_resume() -> None:
        nonlocal has_ps, ps, stdout

        # Resume reading from the recording process.
        nonlocal verbose
        if verbose >= 1:
            sys.stderr.write("Recording.\n")

        handle_fn(settings.simulate_input_code_command, "SETUP")
        ps, stdout = recording_proc_start()
        has_ps = True

    def handle_sig_suspend_from_usr1(_signum: int, _frame: Optional[FrameType]) -> None:
        nonlocal suspend
        if suspend:
            return
        suspend = True
        do_suspend_pause()
        # Use when Py3.6 compatibility is dropped.
        # `signal.raise_signal(signal.SIGSTOP)`
        os.kill(os.getpid(), signal.SIGSTOP)

    def handle_sig_resume_from_cont(_signum: int, _frame: Optional[FrameType]) -> None:
        nonlocal suspend
        if not suspend:
            return
        suspend = False

    def handle_sig_reload_from_hup(_signum: int, _frame: Optional[FrameType]) -> None:
        if verbose >= 1:
            sys.stderr.write("Reload.\n")
        process_fn("")

    import signal

    # Suspend resume from separate signals.
    signal.signal(signal.SIGUSR1, handle_sig_suspend_from_usr1)

    # This allows you to stop via ctrl+z and resume with `fg` at a terminal.
    # This intentionally re-uses the handle_sig_suspend_from_usr1 handler:
    signal.signal(signal.SIGTSTP, handle_sig_suspend_from_usr1)

    signal.signal(signal.SIGCONT, handle_sig_resume_from_cont)

    signal.signal(signal.SIGHUP, handle_sig_reload_from_hup)

    if suspend:
        # Use when Py3.6 compatibility is dropped.
        # `signal.raise_signal(signal.SIGSTOP)`
        os.kill(os.getpid(), signal.SIGSTOP)

    # ---------
    # Main Loop

    if idle_time > 0.0:
        idle_time_prev = time.time()

    while code == 0:
        # -1=cancel, 0=continue, 1=finish.
        code = exit_fn(handled_any)

        # Note that when suspend is enabled the entire process is suspended
        # and this look should not run.
        # This check is simply done to prevent any logic running before the process is actually suspended,
        # although in practice it doesn't look to be a problem.
        if suspend:
            continue

        if idle_time > 0.0:
            # Subtract processing time from the previous loop.
            # Skip idling in the event dictation can't keep up with the recording.
            idle_time_curr = time.time()
            idle_time_test = idle_time - (idle_time_curr - idle_time_prev)
            if idle_time_test > 0.0:
                # Prevents excessive processor load.
                time.sleep(idle_time_test)
                idle_time_prev = time.time()
            else:
                idle_time_prev = idle_time_curr

        # Mostly the data read is quite small (under 1k).
        # Only the 1st entry in the loop reads a lot of data due to the time it takes to initialize the VOSK module.
        try:
            data = stdout.read(block_size)
        except (NameError, ValueError):
            # Start recording if `stdout` is not yet open (NameError), or if it
            # was closed via suspend (ValueError).  This can happen either due
            # to a suspend/resume cycle (SIGUSR1/SIGTSTP->SIGCONT) or when
            # --suspend-on-start was specified followed by a SIGCONT.
            do_suspend_resume()
            continue

        if data:
            ok = rec.AcceptWaveform(data)
            if ok:
                json_text_partial_prev = ""
                json_text = rec_handle_fn_wrapper_from_final_result()
            else:
                json_text, json_text_partial_prev = rec_handle_fn_wrapper_from_partial_result(json_text_partial_prev)

            # Monitor the partial output.
            # Finish if no changes are made for `timeout` seconds.
            if use_timeout:
                if json_text != timeout_text_prev:
                    timeout_text_prev = json_text
                    timeout_time_prev = time.time()
                elif time.time() - timeout_time_prev > timeout:
                    if code == 0:
                        code = 1  # The time was exceeded, exit!

    # Close the recording process.
    if has_ps:
        # stdout.close(), no need, this is exiting.
        os.kill(ps.pid, signal.SIGINT)
        del ps, stdout
        has_ps = False

        # Support setting up input simulation state.
        handle_fn(settings.simulate_input_code_command, "TEARDOWN")

    if code == -1:
        sys.stderr.write("Text input canceled!\n")
        sys.exit(0)

    # This writes many JSON blocks, use the last one.
    rec_handle_fn_wrapper_from_final_result()

    if not progressive:
        # We never arrive here needing deletions
        handle_fn(0, process_fn(" ".join(text_list)))

    return handled_any
