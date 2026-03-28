import argparse
from nerd_dictation.cli._common import argparse_cookie
from nerd_dictation.main import main_cancel

def callback(args: argparse.Namespace) -> None:
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

    argparse_cookie(subparse)

    subparse.set_defaults(func=callback)