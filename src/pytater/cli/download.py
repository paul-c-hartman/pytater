"""This module implements the `pytater download` command, which allows users to download VOSK models for use with the pytater application.

A model is required for dictation to work, and available models can be viewed at https://alphacephei.com/vosk/models. The `download` command simply downloads and extracts a model into the default location used by pytater (using `platformdirs`).
"""

import argparse
from pytater.cli._common import argparse_cookie
from pytater.download_model import main as download_model, MODELS, DEFAULT_MODEL


def callback(args: argparse.Namespace) -> None:
    """Callback function for `pytater download`.
    
    Calls the `download_model` function with the appropriate arguments.

    Args:
        args: The parsed command-line arguments for the `download` command.
    """
    download_model(args.model, args.force, args.confirmation)


def main(subparsers: "argparse._SubParsersAction[argparse.ArgumentParser]") -> None:
    """Sets up arguments for `pytater download` and registers the corresponding callback.

    Args:
        subparsers: The subparsers object from the main argument parser.
    """
    subparse = subparsers.add_parser(
        "download",
        help="Download the VOSK model.",
        description=(
            "This is a helper command to download VOSK models.\n"
            "A model is required for dictation to work. Available models can be viewed at:\n"
            "https://alphacephei.com/vosk/models\n"
            "\n"
            "This simply downloads and extracts a model into the default location used by pytater,\n"
            "which is probably $XDG_CONFIG_DIR/pytater/model\n"
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )

    subparse.add_argument(
        "--model",
        choices=MODELS.keys(),
        default=DEFAULT_MODEL,
        dest="model",
        type=str,
        help=(
            f"The name of the model to download. Defaults to '{DEFAULT_MODEL}'.\n"
            + "These can be found at: https://alphacephei.com/vosk/models.\n"
            + "To use a different model, use the URL to the model file as the argument, for example:\n"
            + ' --model="https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip"\n'
        ),
        required=False,
    )

    subparse.add_argument(
        "--force",
        dest="force",
        default=False,
        action="store_true",
        help=(
            "Force download and unzip the model even if one is already present.\n"
            "This can be useful if the model is corrupted or if you want to update to a newer version of the model.\n"
            "WARNING: will overwrite any existing model without confirmation. Use with caution!"
        ),
        required=False,
    )

    subparse.add_argument(
        "-y",
        dest="confirmation",
        default=False,
        action="store_true",
        help=(
            "Confirm overwriting an existing model.\n" "Use this flag to pass the interactive check if using --force."
        ),
        required=False,
    )

    argparse_cookie(subparse)

    subparse.set_defaults(func=callback)
