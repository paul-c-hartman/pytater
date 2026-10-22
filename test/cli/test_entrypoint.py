import subprocess
import sys


def run_cli(*arguments):
    return subprocess.run(
        [sys.executable, "-m", "pytater", *arguments],
        check=False,
        capture_output=True,
        text=True,
    )


def test_module_entrypoint_help():
    result = run_cli("--help")

    assert result.returncode == 0
    assert "Usage: pytater" in result.stdout


def test_module_entrypoint_version():
    result = run_cli("--version")

    assert result.returncode == 0
    assert result.stdout.strip()


def test_module_entrypoint_unknown_command():
    result = run_cli("does-not-exist")

    assert result.returncode == 1
    assert "Unknown command: does-not-exist" in result.stderr
