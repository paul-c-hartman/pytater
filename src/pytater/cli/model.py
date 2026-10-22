"""This module implements the `pytater model` command, which allows users to download VOSK models for use with the pytater application.

A model is required for dictation to work, and available models can be viewed at https://alphacephei.com/vosk/models. The `model` command simply downloads and extracts a model into the default location used by pytater (using `platformdirs`).
"""

import argparse
from pytater.cli._common import argparse_cookie
from pytater.download_model import main as download_model, DEFAULT_MODEL


def callback(args: argparse.Namespace) -> None:
    """Callback function for `pytater model`.

    Calls the `download_model` function with the appropriate arguments.

    Args:
        args: The parsed command-line arguments for the `model` command.
    """
    download_model(args.model, args.force, args.confirmation)


def main(subparsers: "argparse._SubParsersAction[argparse.ArgumentParser]") -> None:
    """Sets up arguments for `pytater model` and registers the corresponding callback.

    Args:
        subparsers: The subparsers object from the main argument parser.
    """
    subparse = subparsers.add_parser(
        "model",
        help="Manage VOSK models.",
        description=(
            "This is a helper command to list, download, and select VOSK models.\n"
            "A model is required for dictation to work. Available models can be viewed at:\n"
            "https://alphacephei.com/vosk/models\n"
            "\n"
            "Models are stored in the location specified by pytater's configuration,\n"
            "which by default is $XDG_CONFIG_DIR/pytater/model\n"
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )

    subparse.add_argument(
        "--name",
        default=DEFAULT_MODEL,
        dest="model",
        type=str,
        help=(
            f"The name of the model to use. Defaults to '{DEFAULT_MODEL}'.\n"
            + "These can be found at: https://alphacephei.com/vosk/models.\n"
            + "To use a different model, use the URL to the model file as the argument, for example:\n"
            + ' --name="https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip"\n'
        ),
        required=False,
    )

    subparse.add_argument(
        "--url",
        dest="url",
        type=str,
        help=(
            "The URL to the model file to download. This is an alternative to using --name, and if both are provided, --url will take precedence.\n"
            "This can be useful if the model you want to use is not listed on the VOSK models page, or if you want to use a custom model that you have hosted somewhere.\n"
            "Expects a direct link to a zip file containing the model. The zip file should contain the model files directly, not in a subdirectory.\n"
            "For example: `--url=https://example.com/my-model.zip`"
        ),
        required=False,
    )

    subparse.add_argument(
        "--language",
        dest="language",
        type=str,
        help=(
            "The language code of the model to use.\n"
            "These language codes can be found at: https://alphacephei.com/vosk/models.\n"
            "For example: `--language=en-us` specifies a US English model, or `--language=es` specifies a Spanish model.\n"
            "The codes are not consistent so it is suggested to check the website if you do not know the code for your desired language.\n"
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
