"""CLI entry point for Pytater."""

import sys
from pytater.cli import main as start_cli

# Load package version
if sys.version_info < (3, 8):
    from importlib_metadata import version
else:
    from importlib.metadata import version
__version__ = version("pytater")


def main():
    """Main entry point for the Pytater CLI."""
    start_cli(__version__)


if __name__ == "__main__":
    main()
