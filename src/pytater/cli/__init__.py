"""
Pytater.

Usage: pytater [--help | --version] [--cookie=<path>] [--log-level=<level>] <command> [<args>...]

Options:
  -h, --help                 Show this screen.
  -v, --version              Show version.
  --cookie=<path>            Location for writing a temporary cookie (this file is monitored to begin/end dictation) [default: ""]
  --log-level=<level>        Set the logging level. Can be one of: default, verbose, debug [default: default]

Commands:
  begin                      Start the Pytater agent and begin listening for voice commands.
  end                        End dictation. Types in the text recognized so far and terminates the dictation process.
  cancel                     Cancel dictation. Discards the text recognized so far and terminates the dictation process.
  suspend                    Suspend the Pytater agent.
  resume                     Resume the Pytater agent.
  model                      Manage Pytater models.
  help <command>             Show help for a specific command.

For more information, visit the Pytater documentation: https://blog.paulhartman.dev/pytater/

"""

import importlib
import sys
import signal
from docopt import docopt
from pytater.log import logger, set_verbosity as set_log_verbosity


def main(version, argv=sys.argv[1:]):
    """Main entry point for the `pytater` CLI.

    Args:
        version: The version string to display when the `--version` option is used.
        argv: The list of command-line arguments to parse. Default: `sys.argv[1:]`
    """
    # Allow docopt to handle -h/--help and -v/--version
    args = docopt(__doc__, options_first=True, version=version, help=True, argv=argv)

    set_log_verbosity(args["--log-level"])

    # Dispatch to the appropriate sub-command
    command = args["<command>"] or "help"
    command_args = args["<args>"]
    if args["--cookie"] not in (None, "", '""'):
        command_args.extend(["--cookie", args["--cookie"]])
    else:
        command_args.extend(["--cookie", ""])
    try:
        module = importlib.import_module(f"pytater.cli.{command}")
        module.main(docopt(module.__doc__, argv=[command, *command_args]))
    except ModuleNotFoundError:
        logger.error("Unknown command: %s", command)
        sys.exit(1)


def graceful_exit(signum, _frame):
    """Handle graceful exit on SIGINT or SIGTERM."""
    logger.info("Received signal %s. Exiting gracefully...", signum)
    sys.exit(128 + signum)


# Register the signal handlers
signal.signal(signal.SIGINT, graceful_exit)
signal.signal(signal.SIGTERM, graceful_exit)
