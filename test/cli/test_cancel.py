from unittest.mock import patch

from docopt import docopt

from pytater.cli import cancel


def test_cancel_main_forwards_cookie():
    arguments = docopt(cancel.__doc__, argv=["cancel", "--cookie=/tmp/pytater.cookie"])

    with patch("pytater.cli.cancel.main_cancel") as main_cancel:
        cancel.cancel_main(arguments)

    main_cancel.assert_called_once_with(path_to_cookie="/tmp/pytater.cookie")
