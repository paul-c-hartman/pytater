import argparse
from nerd_dictation.cli._common import argparse_cookie
from nerd_dictation.main import main_end

def callback(args: argparse.Namespace) -> None:
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

    argparse_cookie(subparse)

    subparse.set_defaults(func=callback)
