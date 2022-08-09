import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler

LOGGER_FORMAT = (
        "[%(asctime)s] [%(levelname)s] %(name)s %(funcName)s :: "
        + "%(message)s"
)
LOGGING_FORMATTER = logging.Formatter(
    LOGGER_FORMAT, "%Y/%m/%d %H:%M:%S"
)

APP_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))

LOGGING_FILE = os.path.join(PROJECT_ROOT, "logs/scraper.log")


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(LOGGING_FORMATTER)
    return console_handler


def get_file_handler():
    file_handler = TimedRotatingFileHandler(LOGGING_FILE, when="midnight")
    file_handler.setFormatter(LOGGING_FORMATTER)
    return file_handler


def get_logger(logger_name) -> logging.Logger:
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler())
    logger.propagate = False
    return logger
