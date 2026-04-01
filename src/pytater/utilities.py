"""This module provides various utility functions that are used across the pytater application.

These include functions for running commands, handling files, and executing Python scripts.
"""

import subprocess
import sys
import os
import stat
import time
from types import ModuleType
from typing import Optional, IO, List

# -----------------------------------------------------------------------------
# General Utilities


def run_command_or_exit_on_failure(cmd: List[str]) -> None:
    """Run a command and exit with an error message if the command fails.
    
    Args:
        cmd: The command to run, as a list of strings.
    """
    try:
        subprocess.check_output(cmd)
    # Don't catch other kinds of exceptions as they should never happen
    # and can be considered a severe error which doesn't need to be made "user friendly".
    except FileNotFoundError as ex:
        sys.stderr.write(f"Command {cmd[0]!r} not found: {ex}\n")
        sys.exit(1)


def touch(filepath: str, mtime: Optional[int] = None) -> None:
    """Touch a file, creating it if it doesn't exist and updating its modification time.
    
    Args:
        filepath: The path to the file to touch.
        mtime: The modification time to set, or None to use the current time.
    """
    if os.path.exists(filepath):
        os.utime(filepath, None if mtime is None else (mtime, mtime))
    else:
        with open(filepath, "ab") as _:
            pass
        if mtime is not None:
            try:
                os.utime(filepath, (mtime, mtime))
            except FileNotFoundError:
                pass


def file_mtime_or_none(filepath: str) -> Optional[int]:
    """Checks the modification time of a file.

    Args:
        filepath: The path to the file to check.
    
    Returns:
        The modification time of the file, or None if the file does not exist.
    """
    try:
        # For some reason `mypy` thinks this is a float.
        return int(os.stat(filepath)[stat.ST_MTIME])
    except FileNotFoundError:
        return None


def file_age_in_seconds(filepath: str) -> float:
    """Finds the age of the file in seconds.

    Args:
        filepath: The path to the file to check.
    
    Returns:
        The age of the file in seconds.
    """
    return time.time() - os.stat(filepath)[stat.ST_MTIME]


def file_remove_if_exists(filepath: str) -> bool:
    """Removes a file if it exists.

    Args:
        filepath: The path to the file to remove.
    Returns:
        True if the file was removed, False if the file did not exist or could not be removed.
    """
    try:
        os.remove(filepath)
        return True
    except OSError:
        return False


def file_handle_make_non_blocking(file_handle: IO[bytes]) -> None:
    """Make a file handle non-blocking.
    
    Args:
        file_handle: The file handle to make non-blocking.
    """
    import fcntl

    # Get current `file_handle` flags.
    flags = fcntl.fcntl(file_handle.fileno(), fcntl.F_GETFL)
    fcntl.fcntl(file_handle, fcntl.F_SETFL, flags | os.O_NONBLOCK)


def execfile(filepath: str, mod: Optional[ModuleType] = None) -> Optional[ModuleType]:
    """Execute a file path as a Python script.

    Args:
        filepath: The path to the Python script to execute.
        mod: An optional module to execute the script in. If None, a new module will be created.
    
    Returns:
        The module that the script was executed in.
    """
    import importlib.util

    if not os.path.exists(filepath):
        raise FileNotFoundError(f'File not found "{filepath}"')

    mod_name = "__main__"
    mod_spec = importlib.util.spec_from_file_location(mod_name, filepath)
    if mod_spec is None:
        raise RuntimeError(f"Unable to retrieve the module-spec from {filepath!r}")
    if mod is None:
        mod = importlib.util.module_from_spec(mod_spec)

    # While the module name is not added to `sys.modules`, it's important to temporarily
    # include this so statements such as `sys.modules[cls.__module__].__dict__` behave as expected.
    # See: https://bugs.python.org/issue9499 for details.
    modules = sys.modules
    mod_orig = modules.get(mod_name, None)
    modules[mod_name] = mod

    # No error suppression, just ensure `sys.modules[mod_name]` is properly restored in the case of an error.
    try:
        # `mypy` doesn't know about this function.
        mod_spec.loader.exec_module(mod)  # type: ignore
    finally:
        if mod_orig is None:
            modules.pop(mod_name, None)
        else:
            modules[mod_name] = mod_orig

    return mod
