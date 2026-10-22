from unittest.mock import patch

from docopt import docopt

from pytater.cli import resume


def test_resume_main_forwards_cookie_and_resume_action():
    arguments = docopt(resume.__doc__, argv=["resume", "--cookie=/tmp/pytater.cookie"])

    with patch("pytater.cli.resume.main_suspend") as main_suspend:
        resume.resume_main(arguments)

    main_suspend.assert_called_once_with(
        path_to_cookie="/tmp/pytater.cookie",
        suspend=False,
    )
