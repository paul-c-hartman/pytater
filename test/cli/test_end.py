from unittest.mock import patch

from docopt import docopt

from pytater.cli import end


def test_end_main_forwards_cookie():
    arguments = docopt(end.__doc__, argv=["end", "--cookie=/tmp/pytater.cookie"])

    with patch("pytater.cli.end.main_end") as main_end:
        end.end_main(arguments)

    main_end.assert_called_once_with(path_to_cookie="/tmp/pytater.cookie")
