# stdlib
from copy import deepcopy
from pathlib import Path

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json_formatter": {
            "()": "logging_new.logging.GPNJsonFormatter",
            "json_ensure_ascii": False,
        },
        "extended_formatter": {
            "()": "logging_new.logging.ExtraFormatter",
        },
    },
    "handlers": {
        "console_json_handler": {
            "class": "logging.StreamHandler",
            "formatter": "json_formatter",
            "stream": "ext://sys.stdout",
        },
        "console_extended_handler": {
            "class": "logging.StreamHandler",
            "formatter": "extended_formatter",
            "stream": "ext://sys.stdout",
        },
        "file_extended_handler": {
            "class": "logging.FileHandler",
            "formatter": "json_formatter",
            "filename": Path("./labor_exchange/labor_exchange.log"),
            "mode": "w",
        },
    },
    "root": {
        "level": "INFO",
        # хендлеры устанавливаются далее в функциях
        "handlers": ["file_extended_handler", "console_json_handler"],
    },
    "loggers": {
        # отключаем спам логами при генерации данных factoryboy
        "factory": {"level": "WARN"},
        "factory.generate": {"level": "WARN"},
        "faker.factory": {"level": "WARN"},
        "gunicorn.access": {"level": "INFO", "handlers": ["console_json_handler"]},
    },
    "filters": {
        # Уровень debug
        "debugFilter": {"()": "logging_new.logging.LogLevelFilter", "logs_level": 10},
        # Уровень info
        "infoFilter": {"()": "logging_new.logging.LogLevelFilter", "logs_level": 20},
        # Уровень error
        "errorFilter": {"()": "logging_new.logging.LogLevelFilter", "logs_level": 40},
    },
}


def get_raw_output_logging_config() -> dict:
    logger_config = deepcopy(LOGGING)
    logger_config["root"]["handlers"].extend(
        [
            "console_extended_handler",
        ]
    )
    return logger_config


def get_json_output_logging_config() -> dict:
    logger_config = deepcopy(LOGGING)
    logger_config["root"]["handlers"].append("console_json_handler")
    return logger_config
