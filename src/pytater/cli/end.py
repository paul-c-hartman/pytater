import argparse
from pytater.cli._common import argparse_cookie
from pytater.main import main_end


def callback(args: argparse.Namespace) -> None:
    """
    Callback function for `pytater end`. Calls the `main_end` function with the appropriate arguments.
    """
    main_end(
        path_to_cookie=args.path_to_cookie,
    )


def main(subparsers: "argparse._SubParsersAction[argparse.ArgumentParser]") -> None:
    subparse = subparsers.add_parser(
        "end",
        help="End dictation.",
        description="""\
This ends dictation, causing the text to be typed in.
    """,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    """
    Sets up arguments for `pytater end` and registers the corresponding callback.
    """
    argparse_cookie(subparse)

    subparse.set_defaults(func=callback)
