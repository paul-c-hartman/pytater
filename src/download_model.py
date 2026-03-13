import os
import shutil
import tempfile
import urllib.request
import zipfile

MODEL_URL = "https://alphacephei.com/kaldi/models/"
MODELS = {
  "small": "vosk-model-small-en-us-0.15",
  "large": "vosk-model-en-us-0.22",
  "lgraph": "vosk-model-en-us-0.22-lgraph-0.22",
  "gigaspeech": "vosk-model-en-us-0.42-gigaspeech"
}
DEFAULT_MODEL = "small"

def download_and_extract_model(model_url, extract_to):
  with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
    print(f"Downloading model from {model_url}.\nThis may take a minute...")
    urllib.request.urlretrieve(model_url, tmp_file.name)
    print("Download complete. Extracting...")
    with zipfile.ZipFile(tmp_file.name, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print(f"Model extracted to {extract_to}")
  os.remove(tmp_file.name)

def main(model_name=DEFAULT_MODEL, force=False, confirmation=False):
  xdg_config_home = os.getenv('XDG_CONFIG_HOME', os.path.expanduser('~/.config'))
  model_path = os.path.join(xdg_config_home, 'nerd-dictation', 'model')
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
    print(f"Model already exists at {model_path}. No action taken.")