"""This module provides a unified interface for simulating input in the pytater application.

It imports various methods of simulating input, such as using `xdotool`, `ydotool`, `dotool`, `wtype`, and writing directly to stdout. The `input_fns` dictionary maps the names of these methods to their corresponding functions, allowing the rest of the application to easily call the appropriate input simulation method based on user settings or other conditions.
"""

from typing import Callable

from pytater.simulate_input.xdotool import simulate_typing_with_xdotool
from pytater.simulate_input.ydotool import simulate_typing_with_ydotool
from pytater.simulate_input.dotool import simulate_typing_with_dotool, simulate_typing_with_dotoolc
from pytater.simulate_input.wtype import simulate_typing_with_wtype
from pytater.simulate_input.stdout import simulate_typing_with_stdout

input_fns: dict[str, Callable[[int, str], None]] = {
    "XDOTOOL": simulate_typing_with_xdotool,
    "YDOTOOL": simulate_typing_with_ydotool,
    "DOTOOL": simulate_typing_with_dotool,
    "DOTOOLC": simulate_typing_with_dotoolc,
    "WTYPE": simulate_typing_with_wtype,
    "STDOUT": simulate_typing_with_stdout,
}

__all__ = ["input_fns"]
