from nerd_dictation.config import *
from platformdirs import PlatformDirs

def test_config():
    assert settings.all() == {
        "dirs": settings.dirs,
        "temp_cookie_name": settings.temp_cookie_name,
        "simulate_input_code_command": settings.simulate_input_code_command,
    }
    assert settings.dirs.appname == "nerd-dictation"
    assert settings.dirs.appauthor == "paul-c-hartman"
    assert isinstance(settings.dirs, PlatformDirs)
    assert settings.temp_cookie_name == "nerd_dictation.cookie"
    assert settings.simulate_input_code_command == -1