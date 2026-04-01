import io
from contextlib import redirect_stderr
import os
import tempfile
from pytater.download_model import download_progress, download_and_extract_model, set_model
from pytater.config import settings


def test_download_progress_noninteractive():
    f = io.StringIO()
    with redirect_stderr(f):
        download_progress(1, 1024, 10240)
    assert f.getvalue() == ""  # StringIO is not a TTY so nothing


def test_download_progress_interactive():
    f = io.StringIO()
    f.isatty = lambda: True  # Just fake it
    with redirect_stderr(f):
        download_progress(1, 1024, 10240)
    assert f.getvalue() == "\rDownload Progress:  10.0% 1024 / 10240 bytes"


def test_download_progress_unknown_size():
    f = io.StringIO()
    f.isatty = lambda: True  # Just fake it
    with redirect_stderr(f):
        download_progress(1, 1024, -1)
    assert f.getvalue() == "Read 1024 bytes (Total size unknown)\n"


def test_download_and_extract_model():
    # This is a pretty basic test just to make sure the function runs without error and extracts files to the expected location.
    # We won't actually check the contents of the extracted files since that would be testing the zipfile module more than our own code.
    test_model_url = "https://github.com/githubtraining/hellogitworld/archive/refs/heads/master.zip"  # Small, archived, stable link to a valid ZIP for quick downloads
    with tempfile.TemporaryDirectory() as tmp_dir:
        download_and_extract_model(test_model_url, tmp_dir)
        # There should be some files in the model directory
        assert len(os.listdir(tmp_dir)) > 0


def test_set_model():
    # This is a pretty basic test just to make sure the function runs without error and creates the expected symlink.
    symlink_path = os.path.join(settings.dirs.user_data_path, "model")
    backup_path = os.path.join(settings.dirs.user_data_path, "model_backup")
    if os.path.islink(symlink_path):
        # Back up existing symlink if it exists to avoid test interference
        os.replace(symlink_path, backup_path)
    with tempfile.TemporaryDirectory() as tmp_dir:
        set_model(tmp_dir)
        assert os.path.islink(symlink_path)
        assert os.readlink(symlink_path) == tmp_dir

    if os.path.exists(backup_path):
        # Restore original symlink after test
        os.replace(backup_path, symlink_path)
    else:
        # Remove symlink if there was no original
        os.remove(symlink_path)
