"""
Usage: pytater help [<subcommand>]

Show help for a specific subcommand.

"""

import importlib
import sys
from pytater.cli._common import subcommand_handler
from pytater.log import logger


def get_subcommand_help(subcommand):
    if subcommand in ["", None]:
        # General usage
        return importlib.import_module("pytater.cli").__doc__

    try:
        help_text = importlib.import_module(f"pytater.cli.{subcommand}").__doc__
        return help_text
    except ModuleNotFoundError:
        return None


def help_main(arguments):
    """
    Show help for a specific subcommand.
    """
    subcommand = arguments["<subcommand>"]
    help_text = get_subcommand_help(subcommand)
    if help_text is None:
        logger.error("No help available for subcommand '%s'", subcommand)
        sys.exit(1)
    print(help_text.strip())
    sys.exit(0)


main = subcommand_handler("help", help_main)
