"""
Usage: pytater end [--cookie=<path>]

Terminates the dictation process, processing text that has been recognized so far.

Options:
  --cookie=<path>            Location for writing a temporary cookie (this file is monitored to begin/end dictation) [default: ""]

"""

from pytater.cli._common import subcommand_handler
from pytater.main import main_end


def end_main(arguments):
    main_end(path_to_cookie=arguments["--cookie"])


main = subcommand_handler("end", end_main)
