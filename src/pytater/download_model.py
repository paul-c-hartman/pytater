"""This module provides helpers for downloading and managing VOSK speech recognition models for use with the pytater application.
"""

import os
import sys
import shutil
import tempfile
import urllib.request
import zipfile
from .config import settings

MODEL_URL = "https://alphacephei.com/kaldi/models/"
MODELS = {
    "small": "vosk-model-small-en-us-0.15",
    "large": "vosk-model-en-us-0.22",
    "lgraph": "vosk-model-en-us-0.22-lgraph-0.22",
    "gigaspeech": "vosk-model-en-us-0.42-gigaspeech",
}
DEFAULT_MODEL = "small"


def download_progress(block_num: int, block_size: int, total_size: int) -> None:
    """Report download progress to stderr.
    
    Only runs if pytater is running interactively.

    Args:
        block_num: The number of blocks downloaded so far.
        block_size: The size of each block in bytes.
        total_size: The total size of the file in bytes.
    """
    if hasattr(sys, 'ps1'):
        read_so_far = block_num * block_size
        if total_size > 0:
            percent = read_so_far * 1e2 / total_size
            # Use carriage return '\r' to overwrite the current line
            sys.stderr.write(f"\rDownload Progress: {percent:5.1f}% {read_so_far:d} / {total_size:d} bytes")
            if read_so_far >= total_size:
                sys.stderr.write("\n")  # Newline when download is complete
        else:
            sys.stderr.write(f"Read {read_so_far:d} bytes (Total size unknown)\n")
        sys.stderr.flush()


def download_and_extract_model(model_url: str, extract_to: str) -> None:
    """Download a model from the given URL and extract it to the specified directory.
    
    Assumes the URL points to a zip file.

    Args:
        model_url: The URL to download the model from.
        extract_to: The directory to extract the model to.
    """
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        print(f"Downloading model from {model_url}.\nThis may take a minute...")
        urllib.request.urlretrieve(model_url, tmp_file.name, download_progress)
        print("Download complete. Extracting...")
        with zipfile.ZipFile(tmp_file.name, "r") as zip_ref:
            zip_ref.extractall(extract_to)
        # zipfile extracts the model, but the model files are actually
        # in a subfolder named after the model, so we move them up to the expected location and remove the now-empty subfolder.
        extracted_model_folder = os.path.join(extract_to, os.listdir(extract_to)[0])
        for item in os.listdir(extracted_model_folder):
            shutil.move(os.path.join(extracted_model_folder, item), os.path.join(extract_to, item))
        os.rmdir(extracted_model_folder)
        print(f"Model extracted to {extract_to}")
    os.remove(tmp_file.name)


def set_model(directory: str) -> None:
    """Set the model directory by creating a symlink from the path pytater checks to the actual location of the model.

    Args:
        directory: The directory where the model is located.
    """
    # We download models to $XDG_DATA_HOME/pytater/models/{model_name},
    # but the tool tries to load a model from $XDG_DATA_HOME/pytater/model/,
    # so we create a symlink from the expected location to the actual location of the model.
    expected_model_path = os.path.join(settings.dirs.user_data_path, "model")
    # Remove symlink if it exists.
    # This may be a folder
    if os.path.islink(expected_model_path) or os.path.exists(expected_model_path):
        if os.path.isdir(expected_model_path) and not os.path.islink(expected_model_path):
            shutil.rmtree(expected_model_path)
        else:
            os.remove(expected_model_path)
    os.makedirs(os.path.dirname(expected_model_path), exist_ok=True)
    print(f"Symlinking from {expected_model_path} to {directory}")
    os.symlink(directory, expected_model_path)  # os.symlink takes the destination first for some reason


def main(model_name: str = DEFAULT_MODEL, force: bool = False, confirmation: bool = False) -> None:
    """Download a model by name or from a custom URL.

    Args:
        model_name: The name of the model to download, or a custom URL to download from. If the name matches a key in the `MODELS` dictionary, the corresponding model will be downloaded from the predefined URL. Otherwise, the `model_name` will be treated as a custom URL to download from.
        force: Whether to force the download of the model even if it already exists.
        confirmation: Whether the user has confirmed that they want to overwrite an existing model. If `force` is True and `confirmation` is False, the user will be prompted to confirm before overwriting an existing model.
    """
    model_path = os.path.join(settings.dirs.user_data_path, "models")
    model = MODELS.get(model_name, model_name)
    if model is not None:
        # Not a custom URL
        model = f"{MODEL_URL}{model}.zip"
        model_path = os.path.join(model_path, model_name)
    else:
        # Assume it's a custom URL
        print(f"Using custom model URL: {model_name}")
        print("WARNING: The `download` subcommand can only load one custom-URL model at a time.")
        print("Consider using `--vosk-model-dir` when calling `pytater begin` instead.")
        model_path = os.path.join(model_path, "custom_model")

    if not os.path.exists(model_path):
        print("Downloading model...")
        os.makedirs(model_path)
        download_and_extract_model(model, model_path)
    elif force:
        if not confirmation:
            confirm = input("CAUTION: If there is a model present, this will overwrite it. Are you sure? [yN] ")
            if confirm.lower() != "y":
                print("Aborting model download.")
                return
        print("Forcing download of model")
        if os.path.exists(model_path):
            shutil.rmtree(model_path)
        os.makedirs(model_path)
        download_and_extract_model(model, model_path)
    else:
        print(f"Model already exists at {model_path}.")
    set_model(model_path)
