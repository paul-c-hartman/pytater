import sys
from typing import Any, Callable, Union, Dict


def subcommand_handler(
    subcommand: str, handler: Callable[[Dict[str, Any]], Union[None, int]]
) -> Callable[[Dict[str, Any]], None]:
    """Handles the execution of a subcommand.

    Args:
        subcommand: The name of the subcommand to execute.
        handler: A callable that takes the subcommand name and arguments dictionary as parameters.
        arguments: A dictionary of command-line arguments parsed by `docopt`.
    """

    def execute_subcommand(arguments: Dict[str, Any]) -> None:
        """Main entry point for the `pytater {subcommand}` sub-command.

        Args:
            arguments: A dictionary of command-line arguments parsed by `docopt`.
        """

        # Set docstring properly for this handler function
        execute_subcommand.__doc__ = (execute_subcommand.__doc__ or "").format(subcommand=subcommand)

        return_code = handler(arguments)
        if return_code is not None:
            sys.exit(return_code)

    return execute_subcommand
