"""This module implements the `pytater resume` command, which allows users to resume the dictation process after it has been suspended using the `pytater suspend` command.

When the `resume` command is used, recording audio is resumed and the dictation process continues as normal. If pytater is not currently suspended, using the `resume` command will have no effect.
"""

import argparse
from pytater.cli._common import argparse_cookie
from pytater.main import main_suspend


def callback(args: argparse.Namespace) -> None:
    """Callback function for `pytater resume`.
    
    Calls the `main_suspend` function with the appropriate arguments.

    Args:
        args: The parsed command-line arguments for the `resume` command.
    """
    main_suspend(
        path_to_cookie=args.path_to_cookie,
        suspend=False,
        verbose=1,
    )


def main(subparsers: "argparse._SubParsersAction[argparse.ArgumentParser]") -> None:
    """Sets up arguments for `pytater resume` and registers the corresponding callback.

    Args:
        subparsers: The subparsers object from the main argument parser.
    """
    subparse = subparsers.add_parser(
        "resume",
        help="Resume the dictation process.",
        description=(
            "Resume recording audio & the dictation process.\n"
            "\n"
            "This is to be used to resume after the 'suspend' command.\n"
            "When pytater is not suspended, this does nothing.\n"
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )
    argparse_cookie(subparse)

    subparse.set_defaults(func=callback)
