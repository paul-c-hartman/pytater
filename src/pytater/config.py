"""This module defines the configuration for the pytater application.

It includes paths and settings that are used across the application, such as where to store user data and temporary files. The configuration is encapsulated in a `Config` class, and an instance of this class is created as `settings` which can be imported and used throughout the application.

Typical usage example:

    from pytater.config import settings
    print(settings.dirs.user_data_dir)  # Access the user data directory path
    print(settings.temp_cookie_name)     # Access the temporary cookie name
    print(settings.simulate_input_code_command)  # Access the simulate input code command
"""

import os
from typing import Any, Dict
from platformdirs import PlatformDirs
import yaml


class Config:
    """Configuration for pytater.

    This includes paths and other settings that may be used across the application.

    Attributes:
        dirs: An instance of `PlatformDirs` that provides platform-specific directories for storing data, configuration, cache, etc.
        temp_cookie_name: The name of the temporary cookie file used for monitoring Dictation state.
        simulate_input_code_command: The command code used to simulate input, which may be used for triggering actions in the application.
    """

    def __init__(self):
        self.all = self.get_config()
        self._define_properties()

    def load_defaults(self) -> Dict:
        """Load default configuration settings.

        The keys specified in this method determine the configuration settings loaded by this class. All others are ignored. This method can be used to reset the configuration to default values like so: `settings.all = settings.load_defaults()`.

        Returns:
            Dict: A Dictionary containing the default configuration settings.
        """
        dirs = PlatformDirs("pytater", "paul-c-hartman", ensure_exists=True)
        return {
            "dirs": dirs,
            "temp_cookie_name": "pytater.cookie",
            "simulate_input_code_command": -1,
            "config_dir": dirs.user_config_dir,
            "current_model": "vosk-model-small-en-us-0.15",
        }

    def get_config(self) -> Dict[str, Any]:
        """Load user configuration from a file.

        This method reads user configuration from the configuration file, then environment variables, then default values, and updates the settings accordingly.
        """
        config = self.load_defaults()
        config.update(self.load_env_variables())
        # Pass in config dir so user can specify PYTATER_CONFIG_DIR env
        # variable to change where app reads config from.
        # Again, this defaults to XDG_CONFIG_HOME/pytater
        config.update(self.load_user_config(config["config_dir"]))
        return config

    def load_env_variables(self) -> Dict[str, Any]:
        """Load configuration settings from environment variables.

        This method checks for specific environment variables that can override default settings. For example, it checks for `PYTATER_MODEL` to set the `model` setting.

        Returns:
            Dict: A Dictionary containing configuration settings loaded from environment variables.
        """
        config = {}
        # We don't want to override these internal-only settings from environment variables.
        keys_to_skip = ["dirs", "simulate_input_code_command"]
        for key, _value in self.load_defaults().items():
            env_key = f"PYTATER_{key.upper()}"
            if env_key in os.environ and key not in keys_to_skip:
                config[key] = os.environ[env_key]
        return config

    def load_user_config(self, config_dir: str) -> Dict[str, Any]:
        """Load user configuration from a file.

        This method reads user configuration from a file in the specified configuration directory. The configuration file is expected to be in YAML format and named `config.yaml`.

        Args:
            config_dir (str): The directory where the configuration file is located.

        Returns:
            Dict: A Dictionary containing configuration settings loaded from the user configuration file.
        """
        config_path = os.path.join(config_dir, "config.yaml")
        if os.path.exists(config_path):
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    user_config = yaml.safe_load(f)
                    return user_config
            except Exception as e:
                print(f"Error loading user config: {e}")
                return {}
        else:
            return {}

    def _define_properties(self):
        """Define properties for easy access to configuration settings.

        This method defines properties for each configuration setting, allowing for easy access and modification of settings as attributes of the `Config` instance.
        """
        for key, _value in self.load_defaults().items():
            # Define getter only--Config is meant to be read-only after load
            setattr(self.__class__, key, property(lambda self, k=key: self.all[k]))

    # Type annotations for the properties defined in _define_properties
    dirs: PlatformDirs
    temp_cookie_name: str
    simulate_input_code_command: int
    config_dir: str
    current_model: str


settings = Config()
