from platformdirs import PlatformDirs

class Config:
    def __init__(self):
        self.dirs = PlatformDirs("nerd-dictation", "paul-c-hartman", ensure_exists=True)

settings = Config()
