"""This module implements the main entry point for the `pytater` CLI, which provides a command-line interface for controlling the pytater application.

The CLI supports several sub-commands, including `begin`, `end`, `cancel`, `suspend`, `resume`, and `download`. Each sub-command is implemented in its own module within the `pytater.cli` package, and they are all registered with the main argument parser in this module. The CLI allows users to start and stop the dictation process, suspend and resume it as needed, and download VOSK models for use with pytater. The main function in this module is `main`, which serves as the entry point for the CLI.
"""

import argparse
from typing import List, Optional
from pytater.cli.begin import main as argparse_create_begin
from pytater.cli.end import main as argparse_create_end
from pytater.cli.cancel import main as argparse_create_cancel
from pytater.cli.suspend import main as argparse_create_suspend
from pytater.cli.resume import main as argparse_create_resume
from pytater.cli.download import main as argparse_create_download

description = """
This is a utility that activates speech to text on Linux.
While it could use any system currently it uses the VOSK-API.
"""


def argparse_create() -> argparse.ArgumentParser:
    """Creates the main argument parser for the `pytater` CLI, including subparsers for each command.

    Returns:
        An `argparse.ArgumentParser` object configured with the appropriate subparsers and arguments for the `pytater` CLI.
    """
    parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawTextHelpFormatter)

    subparsers = parser.add_subparsers()

    argparse_create_begin(subparsers)

    argparse_create_end(subparsers)
    argparse_create_cancel(subparsers)

    argparse_create_suspend(subparsers)
    argparse_create_resume(subparsers)

    argparse_create_download(subparsers)

    return parser


def main(argv: Optional[List[str]] = None) -> None:
    """Main entry point for the `pytater` CLI.
    
    Parses command-line arguments and dispatches to the appropriate sub-command callback.

    Args:
        argv: A list of command-line arguments to parse. If `None`, the arguments will be taken from `sys.argv`.
    """
    parser = argparse_create()
    args = parser.parse_args(argv)
    # Call sub-parser callback.
    if not hasattr(args, "func"):
        parser.print_help()
        return

    args.func(args)
