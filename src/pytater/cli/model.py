"""
Usage: pytater model [--name=<model> | --url=<url>] [--language=<language>] [--force [-y]] [-l | --list]

Management of VOSK models. A model is required for dictation to work. Available models can be viewed at https://alphacephei.com/vosk/models. Downloads into $XDG_DATA_HOME/pytater/models by default.

Options:
    --name=<model>               Name of the model to download. If not specified, the default model for the current language will be downloaded. See `pytater model --list` for available models [default: {DEFAULT_MODEL}]
    --url=<url>                  URL to the model file to download.
    --language=<language>        Language code for the model to download. It is recommended to check https://alphacephei.com/vosk/models since the language codes are not a consistent format [default: en-us]
    --force                      Force download and unzip the model even if one is already present. This can be useful if the model is corrupted or if you want to update to a newer version of the model. WARNING: This will overwrite any existing model files in the model directory. Use with caution.
    -y, --yes                     Automatically answer yes to the confirmation prompt when using `--force`. Only use this option if you know what you are doing.
    -l, --list                    List available models for the specified language. If no language is specified, lists all available models. Pulled from https://alphacephei.com/vosk/models.

"""

from pytater.cli._common import subcommand_handler
from pytater.download_model import main as download_model, DEFAULT_MODEL

__doc__ = (__doc__ or "").format(DEFAULT_MODEL=DEFAULT_MODEL)


def model_main(arguments):
    download_model(
        model_name=arguments["--name"],
        force=arguments["--force"],
        confirmation=arguments["--yes"],
        # language=arguments["--language"],
    )


main = subcommand_handler("model", model_main)
