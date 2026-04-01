"""This module allows pytater to simulate input by writing directly to stdout.

This is the simplest method of transcription and can be used without any additional dependencies.
"""

import sys
from pytater.config import settings


def simulate_typing_with_stdout(delete_prev_chars: int, text: str) -> None:
    # No setup/tear-down.
    if delete_prev_chars == settings.simulate_input_code_command:
        return

    if delete_prev_chars:
        sys.stdout.write("\x08" * delete_prev_chars)

    sys.stdout.write(text)
    sys.stdout.flush()
