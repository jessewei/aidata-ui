"""logger configuration, AS

Modules:
    Description: Common module to setup logger for a package
    Last update: Jesse Wei, 2025/06/20
    Depenedencies: loguru, logging
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
from typing import Optional
import sys
from pprint import pformat

# if you dont like imports of private modules
# you can move it to typing.py module
from loguru import logger
from loguru._defaults import LOGURU_FORMAT

from .lib_config import cfg_apps

# Default log settings
DEF_LOG_LEVEL = "INFO"
DEF_LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DEF_LOG_DIR = "logs"
DEF_LOG_FILENAME = "app_default.log"


class InterceptHandler(logging.Handler):
    """
    Default handler from examples in loguru documentaion.
    See https://loguru.readthedocs.io/en/stable/overview.html#entirely-compatible-with-standard-logging
    """

    def emit(self, record: logging.LogRecord):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def format_record(record: dict) -> str:
    """
    Custom format for loguru loggers.
    Uses pformat for log any data like request/response body during debug.
    Works with logging if loguru handler it.

    Example:
    >>> payload = [{"users":[{"name": "Nick", "age": 87, "is_active": True}, {"name": "Alex", "age": 27, "is_active": True}], "count": 2}]
    >>> logger.bind(payload=).debug("users payload")
    >>> [   {   'count': 2,
    >>>         'users': [   {'age': 87, 'is_active': True, 'name': 'Nick'},
    >>>                      {'age': 27, 'is_active': True, 'name': 'Alex'}]}]
    """

    format_string = str(LOGURU_FORMAT)
    if record["extra"].get("payload") is not None:
        record["extra"]["payload"] = pformat(
            record["extra"]["payload"], indent=4, compact=True, width=88
        )
        format_string += "\n<level>{extra[payload]}</level>"

    format_string += "{exception}\n"
    return format_string


def setup_logger(
    name: Optional[str] = None,
    level: Optional[str] = None,
    format: Optional[str] = None,
    base_log_folder: Optional[str] = None,
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


def log_flow(logger_name: Optional[str] = None):
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


def init_logging():
    """
    Replaces logging handlers with a handler for using the custom handler.

    WARNING!
    if you call the init_logging in startup event function,
    then the first logs before the application start will be in the old format

    >>> app.add_event_handler("startup", init_logging)
    stdout:
    INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
    INFO:     Started reloader process [11528] using statreload
    INFO:     Started server process [6036]
    INFO:     Waiting for application startup.
    2020-07-25 02:19:21.357 | INFO     | uvicorn.lifespan.on:startup:34 - Application startup complete.

    """

    # disable handlers for specific uvicorn loggers
    # to redirect their output to the default uvicorn logger
    # works with uvicorn==0.11.6
    loggers = (
        logging.getLogger(name)
        for name in logging.root.manager.loggerDict
        if name.startswith("uvicorn.")
    )
    for uvicorn_logger in loggers:
        uvicorn_logger.handlers = []

    # change handler for default uvicorn logger
    intercept_handler = InterceptHandler()
    logging.getLogger("uvicorn").handlers = [intercept_handler]

    # set logs output, level and format
    # logger.configure(
    #     handlers=[{"sink": sys.stdout, "level": logging.DEBUG, "format": format_record}]
    # )
    logger.configure(
        handlers=[
            {
                "sink": sys.stdout,
                "level": logging.DEBUG,
                "format": format_record,
            }  # type: ignore
        ]
    )
