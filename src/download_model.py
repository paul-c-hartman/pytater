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
  "gigaspeech": "vosk-model-en-us-0.42-gigaspeech"
}
DEFAULT_MODEL = "small"

def download_progress(block_num, block_size, total_size):
  if sys.stdin and sys.stdin.isatty():
    read_so_far = block_num * block_size
    if total_size > 0:
      percent = read_so_far * 1e2 / total_size
      # Use carriage return '\r' to overwrite the current line
      sys.stderr.write(f"\rDownload Progress: {percent:5.1f}% {read_so_far:d} / {total_size:d} bytes")
      if read_so_far >= total_size:
        sys.stderr.write('\n') # Newline when download is complete
    else:
      sys.stderr.write(f"Read {read_so_far:d} bytes (Total size unknown)\n")
    sys.stderr.flush()

def download_and_extract_model(model_url, extract_to):
  with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
    print(f"Downloading model from {model_url}.\nThis may take a minute...")
    urllib.request.urlretrieve(model_url, tmp_file.name, download_progress)
    print("Download complete. Extracting...")
    with zipfile.ZipFile(tmp_file.name, 'r') as zip_ref:
      zip_ref.extractall(extract_to)
    # zipfile extracts the model, but the model files are actually
    # in a subfolder named after the model, so we move them up to the expected location and remove the now-empty subfolder.
    extracted_model_folder = os.path.join(extract_to, os.listdir(extract_to)[0])
    for item in os.listdir(extracted_model_folder):
      shutil.move(os.path.join(extracted_model_folder, item), os.path.join(extract_to, item))
    os.rmdir(extracted_model_folder)
    print(f"Model extracted to {extract_to}")
  os.remove(tmp_file.name)

def set_model(directory):
  # We download models to $XDG_DATA_HOME/nerd-dictation/models/{model_name},
  # but the tool tries to load a model from $XDG_DATA_HOME/nerd-dictation/model/,
  # so we create a symlink from the expected location to the actual location of the model.
  expected_model_path = os.path.join(settings.dirs.user_data_path, 'nerd-dictation', 'model')
  # Remove symlink if it exists.
  # This may be a folder
  if os.path.islink(expected_model_path) or os.path.exists(expected_model_path):
    if os.path.isdir(expected_model_path) and not os.path.islink(expected_model_path):
      shutil.rmtree(expected_model_path)
    else:
      os.remove(expected_model_path)
  os.makedirs(os.path.dirname(expected_model_path), exist_ok=True)
  print(f"Symlinking from {expected_model_path} to {directory}")
  os.symlink(directory, expected_model_path) # os.symlink takes the destination first for some reason

def main(model_name=DEFAULT_MODEL, force=False, confirmation=False):
  model_path = os.path.join(settings.dirs.user_data_path, 'nerd-dictation', 'models')
  model = MODELS.get(model_name)
  if model is not None:
    # Not a custom URL
    model = f"{MODEL_URL}{model}.zip"
    model_path = os.path.join(model_path, model_name)
  else:
    # Assume it's a custom URL
    print(f"Using custom model URL: {model_name}")
    print("WARNING: The `download` subcommand can only load one custom-URL model at a time.")
    print("Consider using `--vosk-model-dir` when calling `nerd-dictation begin` instead.")
    model_path = os.path.join(model_path, "custom_model")

  
  if not os.path.exists(model_path):
    print("Downloading model...")
    os.makedirs(model_path)
    download_and_extract_model(model, model_path)
  elif force:
    if not confirmation:
      confirmation = input("CAUTION: If there is a model present, this will overwrite it. Are you sure? [yN] ")
      if confirmation.lower() != 'y':
        print("Aborting model download.")
        return
    print("Forcing download of model")
    shutil.rmtree(model_path) if os.path.exists(model_path) else None
    os.makedirs(model_path)
    download_and_extract_model(model, model_path)
  else:
    print(f"Model already exists at {model_path}.")
  set_model(model_path)