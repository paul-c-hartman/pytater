import argparse
from nerd_dictation.cli._common import argparse_cookie
from nerd_dictation.main import main_suspend

def callback(args: argparse.Namespace) -> None:
    main_suspend(
        path_to_cookie=args.path_to_cookie,
        suspend=False,
        verbose=1,
    )

def main(subparsers: "argparse._SubParsersAction[argparse.ArgumentParser]") -> None:
    subparse = subparsers.add_parser(
        "resume",
        help="Resume the dictation process.",
        description=(
            "Resume recording audio & the dictation process.\n"
            "\n"
            "This is to be used to resume after the 'suspend' command.\n"
            "When nerd-dictation is not suspended, this does nothing.\n"
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )

    argparse_cookie(subparse)

    subparse.set_defaults(func=callback)
