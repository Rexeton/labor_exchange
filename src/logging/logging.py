# stdlib
import datetime
import json
import logging.handlers

# thirdparty
from pythonjsonlogger import jsonlogger

# project
from src.logging.global_fastapi import g
from src.logging.models import GPNLogParamsExtended

# from <core_module>.settings import settings

logger = logging.getLogger("utils-logger")


class LogLevelFilter(logging.Filter):
    def __init__(self, logs_level):
        self.logs_level = logs_level

    def filter(self, record):
        return record.levelno == self.logs_level


class ExtraLoggerAdapter(logging.LoggerAdapter):
    """
    Декоратор для логгера, добавляет extra безусловно для всех лог-записей.

    Пример использования:
    logger = ExtraLoggerAdapter(logger, extra={"new_extra_field": "value_extra_field"})

    logger.error("New log record")
    """

    def process(self, msg, kwargs):
        if "extra" not in kwargs:
            kwargs["extra"] = {}
        kwargs["extra"].update(self.extra)
        return msg, kwargs


class GPNJsonFormatter(jsonlogger.JsonFormatter):
    """
    Форматтер, для добавления поля msg в выходной json. текущий стек парсит только такие логи
    """

    def _get_extra_context_info(self) -> dict:
        extra_info = {}
        if "extra_info_for_logs" in g._vars and g.extra_info_for_logs is not None:
            extra_info.update(g.extra_info_for_logs)
        return extra_info

    def add_fields(self, log_record, record: logging.LogRecord, message_dict):
        super().add_fields(log_record, record, message_dict)

        # добавляем информацию из g
        extra_fields = self._get_extra_context_info()

        message = (
            log_record["message"]
            if not extra_fields.get("err_msg")
            else "Ошибка: " + extra_fields.get("err_msg")
        )

        log_record["asctime"] = datetime.datetime.utcfromtimestamp(record.created)

        log_params_model = GPNLogParamsEvents(
            system_log_type="user" if "user_id" in extra_fields else "application",
            user_id=extra_fields.get("user_id"),
            session_id=extra_fields.get("session_id"),
            company=extra_fields.get("company_name"),
            ms=extra_fields.get("ms"),
            project_name=settings.project_name,
            level=record.levelname,
            message=message
            if "req_method" not in extra_fields or record.levelname == "ERROR"
            else "Обработан http запрос",
            request=extra_fields.get("method"),
            http_referrer=extra_fields.get("url"),
            response_status=extra_fields.get("response_status"),
            request_body=extra_fields.get("request_body"),
            response_body=extra_fields.get("response_body"),
            request_id=extra_fields.get("request_id"),
            well_id=log_record.get("well_id"),
            event_id=log_record.get("event_id"),
            process_name=record.processName,
            thread_name=record.threadName,
        )
        log_record["msg"] = message

        del log_record["message"]

        log_record["logger"] = {}
        log_record["logger"]["name"] = record.name
        log_record["logger"]["level"] = record.levelname

        log_params = log_params_model.to_dict()
        log_record.update(log_params)


class ExtraFormatter(GPNJsonFormatter):
    COMMON_RECORD_ATTRS = [
        "args",
        "created",
        "exc_info",
        "exc_text",
        "filename",
        "funcName",
        "levelname",
        "levelno",
        "linenno",
        "lineno",
        "message",
        "module",
        "msecs",
        "msg",
        "name",
        "pathname",
        "process",
        "processName",
        "relativeCreated",
        "stack",
        "tags",
        "thread",
        "threadName",
        "stack_info",
        "asctime",
        "extra",
        "extra_info",
        "report",
    ]

    def serialize_log_record(self, log_record: dict[str, any]) -> str:
        """
        Необходимо переопределить этот метод таким образом, чтобы не происходила
        сериализация в json строку. Костыль.
        """
        return log_record

    def formatException(self, ei):
        result = super().formatException(ei)
        return result

    def format(self, record):
        s = super().format(record)
        message = (
            datetime.datetime.fromtimestamp(record.created).strftime("%H:%M:%S.%f")
            + " "
            + record.levelname
            + " "
            + s["msg"]
        )
        if record.exc_info:
            message += "\n" + self.formatException(record.exc_info)
        # добавляем отладочную информацию в лог запись
        if s.get("debug_info"):
            message += "\ndebug_info:{0}".format(
                json.dumps(s["debug_info"], ensure_ascii=False, default=str)
            )
        # добавляем extra поля
        extra = {k: v for k, v in record.__dict__.items() if k not in self.COMMON_RECORD_ATTRS}
        extra.update(self._get_extra_context_info())
        if extra:
            message += "\nextra:{0}".format(json.dumps(extra, ensure_ascii=False, default=str))

        return message
