"""CLI entry point for Pytater."""

from importlib.metadata import version
from pytater.cli import main as start_cli

__version__ = version("pytater")


def main():
    """Main entry point for the Pytater CLI."""
    start_cli(__version__)


if __name__ == "__main__":
    main()
