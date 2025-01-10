import logging
from pathlib import Path

LOG_FILE_PATH = Path("~/.nova/logs/nova.log").expanduser()
LOG_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)


def setup_logging():
    """
    Configure the logging settings for Nova.
    """
    logging.basicConfig(
        filename=LOG_FILE_PATH,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    logging.info("Logging setup complete.")


def log_info(message):
    """
    Log an informational message.
    Args:
        message (str): The message to log.
    """
    logging.info(message)


def log_error(message):
    """
    Log an error message.
    Args:
        message (str): The error message to log.
    """
    logging.error(message)


def log_debug(message):
    """
    Log a debug message.
    Args:
        message (str): The debug message to log.
    """
    logging.debug(message)


def log_warning(message):
    """
    Log a warning message.
    Args:
        message (str): The warning message to log.
    """
    logging.warning(message)
