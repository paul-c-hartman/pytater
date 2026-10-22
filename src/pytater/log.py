"""Logging setup for the pytater package.

This module provides logging functionality for the pytater package. It sets up a logger that can be used throughout the package to log messages at various levels (e.g., DEBUG, INFO, WARNING, ERROR, CRITICAL).

Example usage:
    from pytater.log import logger, verbosity, setup_logging

    logger.info("This is an informational message.") #=> (nothing printed)
    logger.debug("This is a debug message.") #=> (nothing printed)
    logger.warning("This is a warning message.") #=> [pytater] WARNING - This is a warning message.
    logger.error("This is an error message.") #=> [pytater] ERROR - This is an error message.
    logger.critical("This is a critical message.") #=> [pytater] CRITICAL - This is a critical message.

    custom_logger = setup_logging(verbosity["debug"])
    custom_logger.debug("This is a debug message from the custom logger.") #=> [pytater] DEBUG - This is a debug message from the custom logger.
"""

import logging


def setup_logging(level: int = logging.INFO) -> logging.Logger:
    """Set up logging for the pytater package.

    Args:
        level (int): The logging level to use. Default is logging.INFO.

    Returns:
        A logger instance for the pytater package.
    """
    logging.basicConfig(level=level, format="[%(name)s] %(levelname)s - %(message)s")
    setup_logger = logging.getLogger("pytater")
    return setup_logger


def set_verbosity(verbosity_level: str) -> None:
    """Set the logging verbosity level for the pytater logger.

    Args:
        verbosity_level (str): The verbosity level to set. Supported values are "default", "verbose", and "debug".
    """
    if verbosity_level not in verbosity:
        logger.warning("Invalid verbosity level %s specified, using default.", verbosity_level)
        verbosity_level = "default"

    logger.setLevel(verbosity[verbosity_level])


verbosity = {"default": logging.WARNING, "verbose": logging.INFO, "debug": logging.DEBUG}

logger = setup_logging()
