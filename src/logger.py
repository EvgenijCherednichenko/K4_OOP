import logging
import logging.config
import typing as t

logger_config = {
    "version": 1,
    "disable_existing_loggers": False,
    # Formatters
    "formatters": {
        "std_format": {
            "format": "{levelname}: {asctime} [{name}] | {message} | File {module}.py, Func {funcName}() on {lineno} line",
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "style": "{",
        }
    },
    # Handlers
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "std_format",
        }
    },
    # Loggers
    "loggers": {
        "hh_parser": {"level": "DEBUG", "handlers": ["console"]},
    }
}

logging.config.dictConfig(logger_config)


def log_data(data: t.List[dict]) -> None:
    logger = logging.getLogger("hh_parser")
    logger.info(data)
