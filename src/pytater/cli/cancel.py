"""This module implements the `pytater cancel` command, which allows users to cancel the dictation process.

When the `cancel` command is used, the text that has been recognized so far is discarded and not typed in, and the dictation process is terminated.
"""

import argparse
from pytater.cli._common import argparse_cookie
from pytater.main import main_cancel


def callback(args: argparse.Namespace) -> None:
    """Callback function for `pytater cancel`.
    
    Calls the `main_cancel` function with the appropriate arguments.

    Args:
        args: The parsed command-line arguments for the `cancel` command.
    """
    main_cancel(
        path_to_cookie=args.path_to_cookie,
    )


def main(subparsers: "argparse._SubParsersAction[argparse.ArgumentParser]") -> None:
    subparse = subparsers.add_parser(
        "cancel",
        help="Cancel dictation.",
        description="This cancels dictation.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    """Sets up arguments for `pytater cancel` and registers the corresponding callback.

    Args:
        subparsers: The subparsers object from the main argument parser.
    """
    argparse_cookie(subparse)

    subparse.set_defaults(func=callback)
