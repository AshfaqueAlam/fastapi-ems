import os
from logging.config import dictConfig

# Define project root and log root. Adjust DJANGO_ROOT to your project base directory.
# PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_ROOT = os.path.join(PROJECT_ROOT, "logs")

# Create required directories if they don't exist.
def setup_log_directories():
    directories = [
        LOG_ROOT,
        os.path.join(LOG_ROOT, "fastapi"),
        os.path.join(LOG_ROOT, "fastapi", "debug"),
        os.path.join(LOG_ROOT, "fastapi", "info"),
        os.path.join(LOG_ROOT, "fastapi", "error"),
        os.path.join(LOG_ROOT, "fastapi", "critical"),
    ]
    for d in directories:
        os.makedirs(d, exist_ok=True)

setup_log_directories()

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] [%(module)s.%(funcName)s] "
                      "[%(process)d.%(thread)d] %(message)s",
            "datefmt": "%d/%b/%Y %H:%M:%S",
        },
        "simple": {
            "format": "[%(asctime)s] %(levelname)s %(message)s",
            "datefmt": "%d/%b/%Y %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "verbose",
        },
        "debug_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(LOG_ROOT, "fastapi", "debug", "fastapi_debug.log"),
            "maxBytes": 2 * 1024 * 1024,  # 2 MB
            "backupCount": 1,
            "level": "DEBUG",
            "formatter": "verbose",
        },
        "info_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(LOG_ROOT, "fastapi", "info", "fastapi_info.log"),
            "maxBytes": 2 * 1024 * 1024,
            "backupCount": 1,
            "level": "INFO",
            "formatter": "verbose",
        },
        "error_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(LOG_ROOT, "fastapi", "error", "fastapi_error.log"),
            "maxBytes": 2 * 1024 * 1024,
            "backupCount": 1,
            "level": "ERROR",
            "formatter": "verbose",
        },
        "critical_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(LOG_ROOT, "fastapi", "critical", "fastapi_critical.log"),
            "maxBytes": 2 * 1024 * 1024,
            "backupCount": 1,
            "level": "CRITICAL",
            "formatter": "verbose",
        },
    },
    "loggers": {
        # Log configuration for your application
        "fastapi": {
            "handlers": ["console", "debug_file", "info_file", "error_file", "critical_file"],
            "level": "DEBUG",  # or get from os.getenv("LOG_LEVEL", "DEBUG")
            "propagate": False,
        },
        # Catch-all logger to catch any logs not explicitly handled.
        "": {
            "handlers": ["info_file"],
            "level": "INFO",
        },
    },
}


def setup_logging():
    dictConfig(LOGGING_CONFIG)
