# core/logger.py

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_DIR = Path("logs")
LOG_FILE = LOG_DIR / "dts_app.log"


def get_logger(name: str = "DTS", level: int = logging.INFO) -> logging.Logger:
    """
    Creates and returns a configured logger with console and rotating file handlers.

    The logger outputs formatted messages to both the terminal and a log file.
    It avoids duplicate handler attachments, which is useful during development
    with tools like Uvicorn's `--reload` option.

    Args:
        name (str): The name of the logger. Defaults to "DTS".
        level (int): Logging level (e.g., logging.INFO, logging.DEBUG). Defaults to logging.INFO.

    Returns:
        logging.Logger: A logger instance configured with stream and rotating file handlers.
    """
    # Ensure the log directory and file exist
    LOG_DIR.mkdir(exist_ok=True)
    LOG_FILE.touch(exist_ok=True)

    # Format the log message
    formatter = logging.Formatter(
        "%(levelname)s:     %(name)s | %(asctime)s | (%(module)s.%(funcName)s) → %(message)s",
        datefmt="%b %d %Y - %I:%M:%S %p",
    )

    # Configure console and rotating file handlers for real-time and persistent logging
    console_handler = logging.StreamHandler()
    file_handler = RotatingFileHandler(LOG_FILE, maxBytes=1_000_000, backupCount=3)
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Create a named logger instance and assign its logging level
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Avoid duplicate handlers (important for uvicorn --reload)
    if not logger.hasHandlers():
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger


def configure_uvicorn_logging(level: int = logging.INFO):
    """
    Redirects uvicorn and FastAPI logs to the same rotating file logger.
    """
    # Ensure the log directory and file exist
    LOG_DIR.mkdir(exist_ok=True)
    LOG_FILE.touch(exist_ok=True)

    uvicorn_loggers = ["uvicorn", "uvicorn.error", "uvicorn.access", "fastapi"]
    for name in uvicorn_loggers:
        uv_logger = logging.getLogger(name)
        uv_logger.setLevel(level)
        if not uv_logger.hasHandlers():
            uv_logger.addHandler(logging.StreamHandler())
            uv_logger.addHandler(
                RotatingFileHandler(LOG_FILE, maxBytes=1_000_000, backupCount=3)
            )
