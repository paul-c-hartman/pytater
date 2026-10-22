"""
Usage: pytater suspend [--cookie=<path>]

Suspends audio recording and dictation when pytater is running. Otherwise has no effect. Can be useful on slower systems where large models take longer to load.

Options:
  --cookie=<path>            Location for writing a temporary cookie [default: ""]

"""

from pytater.cli._common import subcommand_handler
from pytater.main import main_suspend


def suspend_main(arguments):
    main_suspend(path_to_cookie=arguments["--cookie"], suspend=True)


main = subcommand_handler("suspend", suspend_main)
