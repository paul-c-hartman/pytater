import subprocess
import os
from typing import Optional
from nerd_dictation.config import settings

# NOTE: typed as a string for Py3.6 compatibility.
simulate_typing_with_dotool_proc: "Optional[subprocess.Popen[str]]" = None


def simulate_typing_with_dotoolc(delete_prev_chars: int, text: str) -> None:
    simulate_typing_with_dotool(delete_prev_chars, text, cmd="dotoolc")


def simulate_typing_with_dotool(delete_prev_chars: int, text: str, cmd: str = "dotool") -> None:
    if delete_prev_chars == settings.simulate_input_code_command:
        global simulate_typing_with_dotool_proc
        if text == "SETUP":
            # If this isn't true, something strange is going on.
            assert simulate_typing_with_dotool_proc is None
            # "text" was added as a more readable alias for
            # "universal_newlines" in Python 3.7 so use universal_newlines for
            # Python 3.6 compatibility:
            proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, universal_newlines=True)
            assert proc.stdin is not None
            proc.stdin.write("keydelay 4\nkeyhold 0\ntypedelay 12\ntypehold 0\n")
            proc.stdin.flush()
            simulate_typing_with_dotool_proc = proc
        elif text == "TEARDOWN":
            import signal

            assert simulate_typing_with_dotool_proc is not None
            os.kill(simulate_typing_with_dotool_proc.pid, signal.SIGINT)
            # Not needed, just basic hygiene not to keep killed process reference.
            simulate_typing_with_dotool_proc = None
        else:
            raise Exception("Internal error, unknown command {!r}".format(text))
        return

    assert simulate_typing_with_dotool_proc is not None
    proc = simulate_typing_with_dotool_proc
    assert proc.stdin is not None
    if delete_prev_chars:
        proc.stdin.write("key" + (" backspace" * delete_prev_chars) + "\n")
        proc.stdin.flush()

    proc.stdin.write("type " + text + "\n")
    proc.stdin.flush()