# stdlib
import json
import logging
import time
import uuid

import starlette

# thirdparty
from fastapi import status as http_status
from starlette.concurrency import iterate_in_threadpool
from starlette.requests import Request
from starlette.types import Message, Scope

# project
from dependencies.user import get_current_user
from logging_new.global_fastapi import g, set_extra_for_logs
from models import User

logger = logging.getLogger(__name__)


def _bytes_to_json(source: bytes, encoding: str = "utf-8") -> bytes | str | dict | list:
    """
    Функция для преобразования тела запроса и ответа.
    Возвращает копию source или результат преобразования этой копии.
    """
    result = bytes(source)
    try:
        result = result.decode(encoding)
        result = json.loads(result)
    except Exception:
        pass
    return result


class RequestWithBody(Request):
    def __init__(self, scope: Scope, body: bytes) -> None:
        super().__init__(scope, self._receive)
        self._body = body
        self._body_returned = False

    async def _receive(self) -> Message:
        if self._body_returned:
            return {"type": "http.disconnect"}
        else:
            self._body_returned = True
            return {"type": "http.request", "body": self._body, "more_body": False}


class LogRequestInfoMiddleware(starlette.middleware.base.BaseHTTPMiddleware):
    """
    Middleware для логирования информации о запросе, а также о теле запроса и теле ответа (в случае ошибки).
    """

    async def dispatch(self, request, call_next):
        request_body_bytes = await request.body()
        request_with_body = RequestWithBody(request.scope, request_body_bytes)

        try:
            response = await call_next(request_with_body)
        except Exception:
            time1 = time.time()
            request_body = _bytes_to_json(request_body_bytes)
            request_total = round(time1 - g.extra_info_for_logs.get("_request_start", 0), 3)
            # Наверняка будет 500 ошибка, но ответ формируется выше по стеку,
            # и мы доподлинно на этот момент код не знаем; в любом случае информацию по запросу нужно зафиксировать
            extra_kwargs = {
                "response_status": http_status.HTTP_500_INTERNAL_SERVER_ERROR,
                "request_time": request_total,
            }
            set_extra_for_logs(
                {"request_body": request_body, "response_body": None, **extra_kwargs}
            )
            raise
        status = response.status_code

        time1 = time.time()
        request_total = round(time1 - g.extra_info_for_logs.get("_request_start", 0), 3)
        extra_kwargs = {"response_status": status, "request_time": request_total}
        if 400 <= status <= 599:
            if hasattr(response, "body_iterator"):
                response_body_source = [chunk async for chunk in response.body_iterator]
                response.body_iterator = iterate_in_threadpool(iter(response_body_source))
                response_body_bytes = b"".join(response_body_source)
            else:
                # Рассчитываем, что тут Response (где-то же он бывает)
                response_body_bytes = response.body
            response_body = _bytes_to_json(response_body_bytes)
            request_body = _bytes_to_json(request_body_bytes)
            extra_kwargs.update({"request_body": request_body, "response_body": response_body})
        set_extra_for_logs(extra_kwargs)
        return response


class SetRequestContextMiddleware:
    """Middleware для выставления глобальных параметров в контексте запроса."""

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        try:
            request = Request(scope, receive=receive)
            set_extra_for_logs(
                {
                    "request_id": uuid.uuid4(),
                    "_request_start": time.time(),
                    "method": request.method,
                    "url": request.url,
                    "base_url": request.base_url,
                    "query_params": request.query_params,
                }
            )
            # user_info = isinstance(get_current_user(),User)
            # if user_info:
            #     set_extra_for_logs({"session_id": user_info.get("jti"), "user_id": user_info.get("preferred_username")})
            logger.debug("Request started")
        except Exception as e:
            logger.error("Failed setting request context: %s", str(e))
        finally:
            set_extra_for_logs({})

        await self.app(scope, receive, send)
