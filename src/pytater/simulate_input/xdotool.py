"""This module allows pytater to simulate input using the `xdotool` command line utility.
"""

from pytater.utilities import run_command_or_exit_on_failure
from pytater.config import settings


def simulate_typing_with_xdotool(delete_prev_chars: int, text: str) -> None:
    cmd = "xdotool"

    # No setup/tear-down.
    if delete_prev_chars == settings.simulate_input_code_command:
        return

    if delete_prev_chars:
        run_command_or_exit_on_failure(
            [
                cmd,
                "key",
                "--",
                *(["BackSpace"] * delete_prev_chars),
            ]
        )

    run_command_or_exit_on_failure(
        [
            cmd,
            "type",
            "--clearmodifiers",
            "--",
            text,
        ]
    )
