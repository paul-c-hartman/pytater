import argparse
from pytater.cli._common import argparse_cookie
from pytater.main import main_cancel


def callback(args: argparse.Namespace) -> None:
    """
    Callback function for `pytater cancel`. Calls the `main_cancel` function with the appropriate arguments.
    """
    main_cancel(
        path_to_cookie=args.path_to_cookie,
    )


def main(subparsers: "argparse._SubParsersAction[argparse.ArgumentParser]") -> None:
    subparse = subparsers.add_parser(
        "cancel",
        help="Cancel dictation.",
        description="This cancels dictation.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    """
    Sets up arguments for `pytater cancel` and registers the corresponding callback.
    """
    argparse_cookie(subparse)

    subparse.set_defaults(func=callback)
