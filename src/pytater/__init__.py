"""Pytater is a speech recognition application that uses the VOSK library to provide real-time transcription of audio input.

It is meant to be modular, extensible, and easy to use, whether you are a developer looking to integrate speech recognition into your application or a user looking for a simple tool for transcribing speech. It contains utilities for managing active transcription sessions and VOSK models.

For help with the command-line tools, run `pytater --help` or `pytater <subcommand> --help` for more information on a specific subcommand. For help with the Python API, see the docstrings in the code or refer to the [documentation]().
"""

from pytater.main import main_begin, main_end, main_cancel, main_suspend
from pytater.cli import main as main_cli

__all__ = [
    "main_begin",
    "main_end",
    "main_cancel",
    "main_suspend",
    "main_cli",
]
