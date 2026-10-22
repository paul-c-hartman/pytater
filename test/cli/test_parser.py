import importlib

import pytest
from docopt import docopt


@pytest.mark.parametrize("command", ["cancel", "end", "resume", "suspend"])
def test_subcommands_accept_global_cookie_option(command):
    module = importlib.import_module(f"pytater.cli.{command}")

    arguments = docopt(module.__doc__, argv=[command, "--cookie=/tmp/cookie"])

    assert arguments["--cookie"] == "/tmp/cookie"


def test_model_rejects_conflicting_name_and_url():
    module = importlib.import_module("pytater.cli.model")

    with pytest.raises(SystemExit):
        docopt(module.__doc__, argv=["model", "--name=small", "--url=https://example"])


def test_begin_rejects_conflicting_output_modes():
    module = importlib.import_module("pytater.cli.begin")

    with pytest.raises(SystemExit):
        docopt(module.__doc__, argv=["begin", "--defer-output", "--continuous"])
