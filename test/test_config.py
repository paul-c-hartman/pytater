from platformdirs import PlatformDirs
from pytater.config import settings


def test_config():
    assert settings.all() == {
        "dirs": settings.dirs,
        "temp_cookie_name": settings.temp_cookie_name,
        "simulate_input_code_command": settings.simulate_input_code_command,
    }
    assert settings.dirs.appname == "pytater"
    assert settings.dirs.appauthor == "paul-c-hartman"
    assert isinstance(settings.dirs, PlatformDirs)
    assert settings.temp_cookie_name == "pytater.cookie"
    assert settings.simulate_input_code_command == -1
