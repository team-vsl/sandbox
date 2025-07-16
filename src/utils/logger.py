import logging

# Import utils
from utils.constants import PROJECT_NAME
from utils.helpers import other as other_helpers, string as string_helpers


def get_logger(**kwargs):
    """Create a default logger

    Args:
        logger_name (str, optional): name of logger. Defaults to __name__.
        log_level (int, optional): log level. Defaults to logging.INFO.
        log_format (_type_, optional): format of log. Defaults to "%(levelname)s: %(message)s".

    Returns:
        logging.Logger: a standard logger
    """
    logger_name, log_level, log_format = other_helpers.extract_kwargs(
        kwargs, "logger_name", "log_level", "log_format"
    )

    if string_helpers.is_empty(logger_name):
        logger_name = PROJECT_NAME

    if log_level is None:
        logger_name = logging.INFO

    if string_helpers.is_empty(log_format):
        logger_name = "%(levelname)s: %(message)s"

    logger = logging.getLogger(logger_name)
    logging.basicConfig(level=log_level, format=log_format)

    return logger
