from unittest.mock import patch

from docopt import docopt

from pytater.cli import model


def parse_model(arguments):
    return docopt(model.__doc__, argv=["model", *arguments])


def test_model_defaults():
    arguments = parse_model([])

    assert arguments["--name"] == "small"
    assert arguments["--force"] is False
    assert arguments["--yes"] is False
    assert arguments["--list"] is False


def test_model_parses_download_options():
    arguments = parse_model(["--name", "large", "--force", "--yes"])

    assert arguments["--name"] == "large"
    assert arguments["--force"] is True
    assert arguments["--yes"] is True


def test_model_main_translates_arguments_to_downloader():
    with patch("pytater.cli.model.download_model") as download_model:
        model.model_main(parse_model(["--name", "large", "--force", "--yes"]))

    download_model.assert_called_once_with(
        model_name="large",
        force=True,
        confirmation=True,
    )
