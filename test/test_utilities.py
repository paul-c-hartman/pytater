import pytest
from nerd_dictation.utilities import *

def test_run_command_or_exit_on_failure():
    run_command_or_exit_on_failure(["echo", "Hello, World!"])

    with pytest.raises(SystemExit) as exc_info:
        run_command_or_exit_on_failure(["nonexistent_command"])
    assert exc_info.value.code == 1

def test_touch():
    test_file = "__test_touch_file.txt"

    # Ensure the file does not exist before the test.
    if os.path.exists(test_file):
        os.remove(test_file)

    # Touch the file and check if it was created.
    touch(test_file)
    assert os.path.exists(test_file)

    # Get the current mtime of the file.
    original_mtime = int(os.stat(test_file).st_mtime)

    # Touch the file again with a specific mtime and check if it was updated.
    new_mtime = original_mtime - 1000  # Set mtime to 1000 seconds in the past.
    touch(test_file, mtime=new_mtime)
    assert os.stat(test_file).st_mtime == new_mtime

    # Clean up after the test.
    os.remove(test_file)

def test_file_mtime_or_none():
    test_file = "__test_file_mtime_or_none.txt"

    # Ensure the file does not exist before the test.
    if os.path.exists(test_file):
        os.remove(test_file)

    # The function should return None for a non-existent file.
    assert file_mtime_or_none(test_file) is None

    # Create the file and check if the function returns its mtime.
    with open(test_file, "w") as f:
        f.write("Test content")
    mtime = file_mtime_or_none(test_file)
    assert isinstance(mtime, int)

    # Clean up after the test.
    os.remove(test_file)

def test_file_age_in_seconds():
    test_file = "__test_file_age_in_seconds.txt"

    # Ensure the file does not exist before the test.
    if os.path.exists(test_file):
        os.remove(test_file)

    # Create the file and check if the age is close to 0.
    with open(test_file, "w") as f:
        f.write("Test content")
    age = file_age_in_seconds(test_file)
    assert age >= 0

    # Clean up after the test.
    os.remove(test_file)

def test_file_remove_if_exists():
    test_file = "__test_file_remove_if_exists.txt"

    # Ensure the file does not exist before the test.
    if os.path.exists(test_file):
        os.remove(test_file)

    # The function should return False for a non-existent file.
    assert not file_remove_if_exists(test_file)

    # Create the file and check if the function returns True when removing it.
    with open(test_file, "w") as f:
        f.write("Test content")
    assert file_remove_if_exists(test_file)
    assert not os.path.exists(test_file)

def test_file_handle_make_non_blocking():
    import io

    # Create a non-blocking file handle using a pipe.
    r, w = os.pipe()
    r_file = io.open(r, "rb")
    w_file = io.open(w, "wb")

    try:
        # Make the read end of the pipe non-blocking.
        file_handle_make_non_blocking(r_file)

        # Write some data to the pipe and check if it can be read without blocking.
        w_file.write(b"Test data")
        w_file.flush()
        data = r_file.read()
        assert data == b"Test data"
    finally:
        r_file.close()
        w_file.close()

def test_file_handle_make_non_blocking_on_non_blocking_file():
    import io

    # Create a non-blocking file handle using a pipe.
    r, w = os.pipe()
    r_file = io.open(r, "rb")
    w_file = io.open(w, "wb")

    try:
        # Make the read end of the pipe non-blocking.
        file_handle_make_non_blocking(r_file)

        # Make it non-blocking again and check if it doesn't raise an error.
        file_handle_make_non_blocking(r_file)
    finally:
        r_file.close()
        w_file.close()

def test_execfile():
    test_file = "__test_execfile.py"

    # Ensure the file does not exist before the test.
    if os.path.exists(test_file):
        os.remove(test_file)

    # Create a test Python file with some variables.
    with open(test_file, "w") as f:
        f.write("x = 42\ny = 'Hello, World!'")

    # Execute the file and check if the variables are defined in the returned module.
    mod = execfile(test_file)
    assert mod is not None
    assert hasattr(mod, "x")
    assert hasattr(mod, "y")
    assert mod.x == 42
    assert mod.y == "Hello, World!"

    # Clean up after the test.
    os.remove(test_file)
