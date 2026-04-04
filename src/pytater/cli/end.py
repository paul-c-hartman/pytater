"""This module implements the `pytater end` command, which allows users to end the dictation process.

When the `end` command is used, the text that has been recognized so far is typed in, and the dictation process is terminated.
"""

import argparse
from pytater.cli._common import argparse_cookie
from pytater.main import main_end


def callback(args: argparse.Namespace) -> None:
    """Callback function for `pytater end`.
    
    Calls the `main_end` function with the appropriate arguments.

    Args:
        args: The parsed command-line arguments for the `end` command.
    """
    main_end(
        path_to_cookie=args.path_to_cookie,
    )


def main(subparsers: "argparse._SubParsersAction[argparse.ArgumentParser]") -> None:
    """Sets up arguments for `pytater end` and registers the corresponding callback.

    Args:
        subparsers: The subparsers object from the main argument parser.
    """
    subparse = subparsers.add_parser(
        "end",
        help="End dictation.",
        description="""\
This ends dictation, causing the text to be typed in.
    """,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    argparse_cookie(subparse)

    subparse.set_defaults(func=callback)
