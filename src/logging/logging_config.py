# stdlib
from copy import deepcopy

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json_formatter": {
            "()": "<path_to_logging_package>.logger.GPNJsonFormatter",
            "json_ensure_ascii": False,
        },
        "extended_formatter": {
            "()": "<path_to_logging_package>.logger.ExtraFormatter",
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
    },
    "root": {
        "level": "INFO",
        # хендлеры устанавливаются далее в функциях
        "handlers": [],
    },
    "loggers": {
        # отключаем спам логами при генерации данных factoryboy
        "factory": {"level": "WARN"},
        "factory.generate": {"level": "WARN"},
        "faker.factory": {"level": "WARN"},
        "gunicorn.access": {"level": "INFO", "handlers": []},
    },
    "filters": {
        # Уровень debug
        "debugFilter": {"()": "<path_to_logging_package>.logger.LogLevelFilter", "logs_level": 10},
        # Уровень info
        "infoFilter": {"()": "<path_to_logging_package>.logger.LogLevelFilter", "logs_level": 20},
        # Уровень error
        "errorFilter": {"()": "<path_to_logging_package>.logger.LogLevelFilter", "logs_level": 40},
    },
}


def get_raw_output_logging_config() -> dict:
    logger_config = deepcopy(LOGGING)
    logger_config["root"]["handlers"].extend(
        [
            "console_extended_handler",
        ]
    )
    logger_config["loggers"]["gunicorn.access"]["handlers"].extend(
        [
            "console_extended_handler",
        ]
    )
    return logger_config


def get_json_output_logging_config() -> dict:
    logger_config = deepcopy(LOGGING)
    logger_config["root"]["handlers"].append("console_json_handler")
    logger_config["loggers"]["gunicorn.access"]["handlers"].append("console_json_handler")
    return logger_config
