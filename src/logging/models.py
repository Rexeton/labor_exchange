# stdlib
import dataclasses
import uuid
from typing import Literal


@dataclasses.dataclass
class GPNLogParams:
    """
    Датакласс, описывающий поля логирования, требуемые документом
    https://kb.gazprom-neft.local/pages/viewpage.action?pageId=247900567&preview=/247900567/247900571/%D0%9F%D1%80%D0%B8%D0%BB%D0%BE%D0%B6%D0%B5%D0%BD%D0%B8%D0%B5%203.docx
    """

    # 2 Тип лога log_type user user/application application user
    system_log_type: Literal["user", "application"] = "application"
    # 4 Логин AD user_id Ivanov.II text + keyword
    user_id: str | None = None
    # 8 Идентификатор сессии session_id text + keyword
    session_id: str | None = None
    # 12 Дочернее общество (при наличии) company text + keyword
    company: str | None = None
    # 13 Месторождение (при наличии) ms Идентификатор НСИ text + keyword
    ms: str | None = None
    # 15 Имя проекта (при наличии) project_name
    project_name: str | None = None
    # 16 Уровень события level ERROR, WARNING, INFO, ATTENTION, ... text + keyword
    level: str | None = None
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
    # 24 Идентификатор задачи от пользователя
    task_id_by_user: str | None = None
    # 25 Наименование задачи от пользователя
    task_name_by_user: str | None = None

    def to_dict(self, exclude_none: bool = False):
        if exclude_none:
            return {key: value for key, value in dataclasses.asdict(self).items() if value}
        return dataclasses.asdict(self)


@dataclasses.dataclass
class GPNLogParamsExtended(GPNLogParams):
    """Датакласс, дополняющий описание логов полезными для сервиса полями."""

    request_id: uuid.UUID | None = None
    well_id: uuid.UUID | None = None
    event_id: uuid.UUID | None = None
    process_name: str | None = None
    thread_name: str | None = None
