"""
Usage: pytater resume [--cookie=<path>]

Resumes audio recording and dictation when pytater is suspended. Otherwise has no effect.

Options:
  --cookie=<path>            Location for writing a temporary cookie [default: ""]

"""

from pytater.cli._common import subcommand_handler
from pytater.main import main_suspend


def resume_main(arguments):
    main_suspend(path_to_cookie=arguments["--cookie"], suspend=False)


main = subcommand_handler("resume", resume_main)
