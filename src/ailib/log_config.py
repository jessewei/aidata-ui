"""logger configuration, AS

Modules:
    Description: Common module to setup logger for a package
    Last update: Jesse Wei, 2025/02/13
    setup_logger: Setup logger for a package
    log_flow: Decorator to log function flow
    DEF_LOG_LEVEL : "INFO"
    DEF_LOG_FORMAT : "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    DEF_LOG_DIR : "logs"
    DEF_LOG_FILENAME : "app_default.log"
"""

import logging
import logging.handlers

from pathlib import Path
from ailib.cfg_lib import cfg_apps

# Default log settings
DEF_LOG_LEVEL = "INFO"
DEF_LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DEF_LOG_DIR = "logs"
DEF_LOG_FILENAME = "app_default.log"


def setup_logger(
    name: str = None, level: str = None, format: str = None, base_log_folder: str = None
) -> logging.Logger:
    """Setup logger for a package

    Args:
        name (str, optional): application name. Defaults to None.

    Returns:
        logging.Logger: the application logger
    """
    log_config = cfg_apps.get("logging", {})

    if level is None:
        log_level = getattr(logging, log_config.get("level", DEF_LOG_LEVEL).upper())
    else:
        log_level = getattr(logging, level.upper())

    if format is None:
        log_format = log_config.get("format", DEF_LOG_FORMAT)
    else:
        log_format = format

    if base_log_folder is None:
        log_base_log_folder = log_config.get("base_log_folder", DEF_LOG_DIR)
    else:
        log_base_log_folder = base_log_folder

    if name is None:
        name = f'{__name__}'
        log_filename_template = log_config.get("log_filename_template")
        if log_filename_template is None:
            filename = log_config.get("filename", DEF_LOG_FILENAME)
        else:
            filename = eval(f"f'{log_filename_template}'")
    else:
        filename = f"{name}.log"

    log_filename = Path(log_base_log_folder) / filename
    rotation_size = int(log_config.get("rotation", "10MB").strip("MB")) * 1024 * 1024

    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    # Disable handler inheritance from the root logger
    # logger.propagate = False

    # Prevent duplicate handlers
    # if logger.hasHandlers():  # fail with unknown issue
    #     return logger
    if logger.handlers != []:
        return logger

    # Create formatter
    formatter = logging.Formatter(log_format)

    # File handler with rotation
    file_handler = logging.handlers.RotatingFileHandler(
        log_filename, maxBytes=rotation_size, backupCount=5
    )
    file_handler.setFormatter(formatter)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Attach handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


def log_flow(logger_name: str = None):
    """Decorator to log function flow

    Args:
        logger_name (str, optional): logger name. Defaults to None.

    Returns:
        func: wrapper function
    """
    if logger_name is not None:
        logger = setup_logger(logger_name)
    else:
        logger = setup_logger()
    logger.level = logging.DEBUG

    # def decorator(func):  # Inner decorator function
    #     def wrapper(*args, **kwargs):
    #         logging.debug(f"FLOW: {func.__name__} called with args {args}, kwargs {kwargs}")
    #         return func(*args, **kwargs)

    #     return wrapper
    def decorator(func):
        def wrapper(*args, **kwargs):
            logger = logging.getLogger(logger_name)
            logger.debug(f"FLOW: Entering: {func.__name__}")
            result = func(*args, **kwargs)
            logger.debug(f"FLOW: Exiting: {func.__name__}")
            return result

        return wrapper

    return decorator
