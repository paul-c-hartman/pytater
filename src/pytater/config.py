"""This module defines the configuration for the pytater application.

It includes paths and settings that are used across the application, such as where to store user data and temporary files. The configuration is encapsulated in a `Config` class, and an instance of this class is created as `settings` which can be imported and used throughout the application.

Typical usage example:

    from pytater.config import settings
    print(settings.dirs.user_data_dir)  # Access the user data directory path
    print(settings.temp_cookie_name)     # Access the temporary cookie name
    print(settings.simulate_input_code_command)  # Access the simulate input code command
"""

from platformdirs import PlatformDirs
from typing import Any


class Config:
    """Configuration for pytater.
    
    This includes paths and other settings that may be used across the application.

    Attributes:
        dirs: An instance of `PlatformDirs` that provides platform-specific directories for storing data, configuration, cache, etc.
        temp_cookie_name: The name of the temporary cookie file used for monitoring dictation state.
        simulate_input_code_command: The command code used to simulate input, which may be used for triggering actions in the application.
    """
    def __init__(self):
        self.dirs = PlatformDirs("pytater", "paul-c-hartman", ensure_exists=True)
        self.temp_cookie_name = "pytater.cookie"
        self.simulate_input_code_command = -1

    def all(self) -> dict[str, Any]:
        """Get all configuration settings.

        Returns:
            A dictionary containing all configuration settings.
        """
        return {
            "dirs": self.dirs,
            "temp_cookie_name": self.temp_cookie_name,
            "simulate_input_code_command": self.simulate_input_code_command,
        }


settings = Config()
