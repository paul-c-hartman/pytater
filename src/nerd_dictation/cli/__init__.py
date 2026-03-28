import argparse
from typing import List, Optional
from nerd_dictation.cli.begin import main as argparse_create_begin
from nerd_dictation.cli.end import main as argparse_create_end
from nerd_dictation.cli.cancel import main as argparse_create_cancel
from nerd_dictation.cli.suspend import main as argparse_create_suspend
from nerd_dictation.cli.resume import main as argparse_create_resume
from nerd_dictation.cli.download import main as argparse_create_download

description = """
This is a utility that activates speech to text on Linux.
While it could use any system currently it uses the VOSK-API.
"""


def argparse_create() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawTextHelpFormatter)

    subparsers = parser.add_subparsers()

    argparse_create_begin(subparsers)

    argparse_create_end(subparsers)
    argparse_create_cancel(subparsers)

    argparse_create_suspend(subparsers)
    argparse_create_resume(subparsers)

    argparse_create_download(subparsers)

    return parser


def main(argv: Optional[List[str]] = None) -> None:
    parser = argparse_create()
    args = parser.parse_args(argv)
    # Call sub-parser callback.
    if not hasattr(args, "func"):
        parser.print_help()
        return

    args.func(args)
