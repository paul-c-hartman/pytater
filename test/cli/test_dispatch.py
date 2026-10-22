from unittest.mock import patch

import pytest

from pytater import cli
from pytater.cli import cancel


def test_main_dispatches_command_and_forwards_cookie():
    with patch("pytater.cli.cancel.main") as command_main:
        with patch("pytater.cli.importlib.import_module", return_value=cancel):
            cli.main("1.2.3", ["--log-level=debug", "--cookie=/tmp/cookie", "cancel"])

    command_main.assert_called_once_with({"--cookie": "/tmp/cookie", "cancel": True})


def test_main_reports_unknown_command(caplog):
    with patch(
        "pytater.cli.importlib.import_module",
        side_effect=ModuleNotFoundError("unknown command"),
    ):
        with pytest.raises(SystemExit) as error:
            cli.main("1.2.3", ["does-not-exist"])

    assert error.value.code == 1
    assert "Unknown command: does-not-exist" in caplog.text


def test_main_help_exits_successfully(capsys):
    with pytest.raises(SystemExit) as error:
        cli.main("1.2.3", ["--help"])

    assert error.value.code is None
    assert "Usage: pytater" in capsys.readouterr().out


def test_main_version_exits_successfully(capsys):
    with pytest.raises(SystemExit) as error:
        cli.main("1.2.3", ["--version"])

    assert error.value.code is None
    assert capsys.readouterr().out.strip() == "1.2.3"
