from unittest.mock import patch

from docopt import docopt

from pytater.cli import suspend


def test_suspend_main_forwards_cookie_and_suspend_action():
    arguments = docopt(suspend.__doc__, argv=["suspend", "--cookie=/tmp/pytater.cookie"])

    with patch("pytater.cli.suspend.main_suspend") as main_suspend:
        suspend.suspend_main(arguments)

    main_suspend.assert_called_once_with(
        path_to_cookie="/tmp/pytater.cookie",
        suspend=True,
    )
