"""This module allows pytater to simulate input using the `ydotool` command line utility.
"""

from pytater.utilities import run_command_or_exit_on_failure
from pytater.config import settings


def simulate_typing_with_ydotool(delete_prev_chars: int, text: str) -> None:
    cmd = "ydotool"

    # No setup/tear-down.
    if delete_prev_chars == settings.simulate_input_code_command:
        return

    if delete_prev_chars:
        # ydotool's key subcommand works with int key IDs and key states. 14 is
        # the linux keycode for the backspace key, and :1 and :0 respectively
        # stand for "pressed" and "released."
        #
        # The key delay is lower than the typing setting because it applies to
        # each key state change (pressed, released).
        run_command_or_exit_on_failure(
            [
                cmd,
                "key",
                "--key-delay",
                "3",
                "--",
                *(["14:1", "14:0"] * delete_prev_chars),
            ]
        )

    # The low delay value makes typing fast, making the output much snappier
    # than the slow default.
    run_command_or_exit_on_failure(
        [
            cmd,
            "type",
            "--next-delay",
            "5",
            "--",
            text,
        ]
    )
