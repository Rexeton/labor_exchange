# stdlib
import dataclasses
import uuid
from typing import Literal


@dataclasses.dataclass
class GPNLogParams:
    """
    Датакласс, описывающий поля логирования, требуемые документом
    """

    # 4 Логин AD user_id Ivanov.II text + keyword
    user_id: str | None = None
    # 8 Идентификатор сессии session_id text + keyword
    session_id: str | None = None
    # 12 Дочернее общество (при наличии) company text + keyword
    company: str | None = None
    # 17 Детальное сообщение message Выполнен вход,
    # Загрузка параметров по IPR, Обновлён проект, Ошибка в работе модуля ВР -
    # ResponseError(..., Ошибка при выгрузке отчета – Error code ...,
    # Ошибка в работе модуля - ErrorCode...,
    # Ошибка при запуске расчета: Текст ошибуи ErrorCode...,и т.п.text
    message: str | None = None
    # 18 Статус события (при наличии) status Рассчитано,Ошибка,В процессе, ...text + keyword
    status: str | None = None
    # 19 Метод HTTP request POST, GET..text + keyword
    request: str | None = None
    # 20 URL запроса http_referrer http://hostport/api/config?args=1
    http_referrer: str | None = None
    # 21 Код статуса ответа API response_status 200, 302, 400, 502... Number integer
    response_status: str | None = None
    # 22 Тело запроса для статусов 4**, 5** request_body {...} text + keyword
    request_body: bytes | str | dict | list | None = None
    # 23 Тело ответа для статусов 4**, 5** response_body для статусов 4**, 5**{...} text + keyword
    response_body: bytes | str | dict | list | None = None
    24
    elapsed_time: float | None = None
    request_id: str | None = None
    _request_start: str | None = None
    method: str | None = None
    url: str | None = None
    base_url: str | None = None
    query_params: str | None = None

    def to_dict(self, exclude_none: bool = False):
        if exclude_none:
            return {key: value for key, value in dataclasses.asdict(self).items() if value}
        return dataclasses.asdict(self)


@dataclasses.dataclass
class GPNLogParamsExtended(GPNLogParams):
    """Датакласс, дополняющий описание логов полезными для сервиса полями."""
