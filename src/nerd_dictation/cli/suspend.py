import argparse
from nerd_dictation.cli._common import argparse_cookie
from nerd_dictation.main import main_suspend

def callback(args: argparse.Namespace) -> None:
    main_suspend(
        path_to_cookie=args.path_to_cookie,
        suspend=True,
        verbose=1,
    )

def main(subparsers: "argparse._SubParsersAction[argparse.ArgumentParser]") -> None:
    subparse = subparsers.add_parser(
        "suspend",
        help="Suspend the dictation process.",
        description=(
            "Suspend recording audio & the dictation process.\n"
            "\n"
            "This is useful on slower systems or when large language models take longer to load.\n"
            "Recording audio is stopped and the process is paused to remove any CPU overhead."
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )

    argparse_cookie(subparse)

    subparse.set_defaults(func=callback)