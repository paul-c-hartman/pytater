"""This module allows pytater to simulate input using the `wtype` command line utility.
"""

from pytater.utilities import run_command_or_exit_on_failure
from pytater.config import settings


def simulate_typing_with_wtype(delete_prev_chars: int, text: str) -> None:
    cmd = "wtype"

    # No setup/tear-down.
    if delete_prev_chars == settings.simulate_input_code_command:
        return

    if delete_prev_chars:
        run_command_or_exit_on_failure(
            [
                cmd,
                "-s",
                "5",
                *(["-k", "backSpace"] * delete_prev_chars),
            ]
        )

    run_command_or_exit_on_failure(
        [
            cmd,
            text,
        ]
    )
