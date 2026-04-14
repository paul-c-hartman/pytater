import os
from typing import Optional
from contextlib import redirect_stdout
from functools import cache
import io
import vosk
from pytater.config import settings
from pytater.logging import logger

# On first loading the VOSK package, we want to ensure that it knows where we're keeping models
# and isn't downloading them to some other location. This is a bit hacky, but it works.
# This is why we import this file when loading VOSK for data processing as well.
vosk.MODEL_DIRS = os.path.join(settings.dirs.user_data_path, "models")


@cache
def list_available_models(language: Optional[str] = "en-us") -> list:
    """List available Vosk models for a given language.

    Args:
        language (str): The language code (e.g., "en-us" for English). If None, lists models for all languages.
        For a complete list of language codes, use list_available_languages().


    Returns:
        list: A list of available model names.
    """
    # The VOSK package provides this functionality, but it's
    # not quite what we need. They print the list to stdout.
    f = io.StringIO()
    with redirect_stdout(f):
        vosk.list_models()
    output = f.getvalue()
    models = []
    if language is None:
        language = ""
    for line in output.splitlines():
        if language in line:
            model_name = line.strip()
            models.append(model_name)
    return models


@cache
def list_available_languages() -> list:
    """List available languages for Vosk models.

    Returns:
        list: A list of available language codes.
    """
    # This is similar to list_available_models, since the VOSK
    # package prints these to stdout for some reason.
    f = io.StringIO()
    with redirect_stdout(f):
        vosk.list_languages()
    output = f.getvalue()
    languages = []
    for line in output.splitlines():
        language_code = line.strip()
        languages.append(language_code)
    return languages


def load_model(model_name: Optional[str] = None, language: Optional[str] = None) -> vosk.Model:
    """Load a Vosk model by name or language.

    If the model name is provided, it will be used; otherwise, the language code will
    be used to find a suitable model. If neither is provided, the default language "en-us" will be used.

    Args:
        model_name (str): The name of the model to load.
        language (str): The language code for the model (e.g., "en-us" for English). Only used if model_name is None. If None, defaults to "en-us".
    Returns:
        vosk.Model: The loaded Vosk model.
    """
    if model_name is not None:
        logger.info("Loading model %r...", model_name)
        # Even though VOSK narrates the loading/download process,
        # this is not a problem since it runs either:
        # 1. When a user runs a model management command, in which case they expect to see output, or
        # 2. When the library is processing data, in which case this is running in a separate process and the output is not visible to the user.
        model = vosk.Model(model_name=model_name)
        logger.info("Model %r loaded successfully.", model_name)
        return model
    else:
        if language is None:
            language = "en-us"
        logger.info("Loading model for language %r...", language)
        model = vosk.Model(lang=language)
        logger.info("Model for language %r loaded successfully.", language)
        return model
