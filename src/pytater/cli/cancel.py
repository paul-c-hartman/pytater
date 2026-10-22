"""
Usage: pytater cancel [--cookie=<path>]

Terminates the dictation process, discarding text that has been recognized so far.

Options:
  --cookie=<path>            Location for writing a temporary cookie (this file is monitored to begin/end dictation) [default: ""]

"""

from pytater.main import main_cancel
from pytater.cli._common import subcommand_handler


def cancel_main(arguments):
    main_cancel(path_to_cookie=arguments["--cookie"])


main = subcommand_handler("cancel", cancel_main)
