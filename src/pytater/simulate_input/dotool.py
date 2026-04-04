"""This module allows pytater to simulate input using the `dotool` command line utility or `dotoolc`, which is dotool's background service."""

import subprocess
import os
from typing import Optional
from pytater.config import settings

# NOTE: typed as a string for Py3.6 compatibility.
simulate_typing_with_dotool_proc: "Optional[subprocess.Popen[str]]" = None


class DotoolProcess:
    """Manages a dotool process, allowing for idempotent start and teardown."""

    def __init__(self, cmd: str = "dotool") -> None:
        self.cmd = cmd
        self.proc: Optional[subprocess.Popen[str]] = None

    def ensure_started(self) -> None:
        """Idempotent start, does nothing if already started."""
        if self.proc is not None:
            return
        self.proc = get_dotool_process(self.cmd)

    def write(self, text: str) -> None:
        """Write text to the dotool process, ensuring it is started first."""
        self.ensure_started()
        assert self.proc is not None
        assert self.proc.stdin is not None
        self.proc.stdin.write(text)
        self.proc.stdin.flush()

    def __enter__(self) -> "DotoolProcess":
        self.ensure_started()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        # We actually want to keep the reference around until
        # we decide we want to teardown
        pass

    def teardown(self) -> None:
        """Idempotent teardown, does nothing if not started.

        Removes the process reference after killing it. The same object can be reused,
        just call `ensure_started()` again to start a new process.
        """
        if self.proc is None:
            return
        import signal

        assert self.proc is not None
        os.kill(self.proc.pid, signal.SIGINT)
        # Not needed, just basic hygiene not to keep killed process reference.
        self.proc = None


dotool_process = DotoolProcess()
dotoolc_process = DotoolProcess(cmd="dotoolc")


def simulate_typing_with_dotoolc(delete_prev_chars: int, text: str) -> None:
    simulate_typing_with_dotool(delete_prev_chars, text, process=dotoolc_process)


def get_dotool_process(cmd: str = "dotool") -> Optional[subprocess.Popen[str]]:
    """Get the current dotool process if it exists.

    Returns:
        The current dotool process if it exists, otherwise None.
    """
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, universal_newlines=True)
    assert proc.stdin is not None
    proc.stdin.write("keydelay 4\nkeyhold 0\ntypedelay 12\ntypehold 0\n")
    proc.stdin.flush()
    return proc


def simulate_typing_with_dotool(delete_prev_chars: int, text: str, process: DotoolProcess = dotool_process) -> None:
    if delete_prev_chars == settings.simulate_input_code_command:
        if text == "SETUP":
            # # If this isn't true, something strange is going on.
            # assert proc is None
            process.ensure_started()
        elif text == "TEARDOWN":
            process.teardown()
        else:
            raise RuntimeError(f"Internal error, unknown command {text}")
        return

    with process:
        if delete_prev_chars:
            process.write("key" + (" backspace" * delete_prev_chars) + "\n")
        process.write("type " + text + "\n")
