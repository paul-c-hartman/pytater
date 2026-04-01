"""This module implements the `pytater suspend` command, which allows users to suspend the dictation process.

This can be useful on slower systems or when large language models take longer to load. When the `suspend` command is used, recording audio is stopped and the process is paused to remove any CPU overhead.
"""

import argparse
from pytater.cli._common import argparse_cookie
from pytater.main import main_suspend


def callback(args: argparse.Namespace) -> None:
    """Callback function for `pytater suspend`.
    
    Calls the `main_suspend` function with the appropriate arguments.

    Args:
        args: The parsed command-line arguments for the `suspend` command.
    """
    main_suspend(
        path_to_cookie=args.path_to_cookie,
        suspend=True,
        verbose=1,
    )


def main(subparsers: "argparse._SubParsersAction[argparse.ArgumentParser]") -> None:
    subparse = subparsers.add_parser(
        "suspend",
        help="Suspend the dictation process.",
        description=(
            "Suspend recording audio & the dictation process.\n"
            "\n"
            "This is useful on slower systems or when large language models take longer to load.\n"
            "Recording audio is stopped and the process is paused to remove any CPU overhead."
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )
    """Sets up arguments for `pytater suspend` and registers the corresponding callback.

    Args:
        subparsers: The subparsers object from the main argument parser.
    """
    argparse_cookie(subparse)

    subparse.set_defaults(func=callback)
