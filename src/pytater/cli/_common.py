"""This module contains common code used by multiple subcommands in the `pytater` CLI.
"""

import argparse


def argparse_cookie(subparse: argparse.ArgumentParser) -> None:
    """Add the `--cookie` argument to the given subparser.
    
    This argument is used to specify the location of a temporary cookie file that is monitored to begin/end dictation.

    Args:
        subparse: The argument parser to which the `--cookie` argument should be added.
    """
    subparse.add_argument(
        "--cookie",
        dest="path_to_cookie",
        default="",
        type=str,
        metavar="FILE_PATH",
        help="Location for writing a temporary cookie (this file is monitored to begin/end dictation).",
        required=False,
    )
