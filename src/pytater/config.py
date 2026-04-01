from platformdirs import PlatformDirs
from typing import Any


class Config:
    """
    Configuration for pytater. This includes paths and other settings that may be used across the application.
    """
    def __init__(self):
        self.dirs = PlatformDirs("pytater", "paul-c-hartman", ensure_exists=True)
        self.temp_cookie_name = "pytater.cookie"
        self.simulate_input_code_command = -1

    def all(self) -> dict[str, Any]:
        """
        Returns all configuration settings as a dictionary.
        """
        return {
            "dirs": self.dirs,
            "temp_cookie_name": self.temp_cookie_name,
            "simulate_input_code_command": self.simulate_input_code_command,
        }


settings = Config()
