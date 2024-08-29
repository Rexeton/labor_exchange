"""Module of schemas of jobs"""

import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic.class_validators import root_validator


def salary_match(cls, values):
    if values["salary_to"] < values["salary_from"]:
        raise ValueError(
            "Некорректные данные по зарплате: зарплата сверху {} меньше чем снизу {}".format(
                values["salary_to"], values["salary_from"]
            )
        )
    if values["salary_from"] < 0:
        raise ValueError(
            "Некорректные данные по зарплате: зарплата {} меньше нуля".format(values["salary_from"])
        )
    return values


class JobSchema(BaseModel):
    """Shema of model"""

    id: int
    user_id: int
    title: str
    discription: str
    salary_from: int
    salary_to: int
    is_active: bool
    created_at: datetime.datetime

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "user_id": 2,
                "title": "Povar",
                "discription": "Salat rezat",
                "salary_from": 0,
                "salary_to": 10,
                "is_active": True,
                "created_at": "2024-08-06T20:41:48.521Z",
            }
        }


class JobCreateSchema(BaseModel):
    """Shema to create model"""

    title: str
    discription: str
    salary_from: int = 0
    salary_to: int = 0
    is_active: bool = True

    _salary_validation_ = root_validator(allow_reuse=True)(salary_match)

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "title": "Povar",
                "discription": "Salat rezat",
                "salary_from": 0,
                "salary_to": 10,
                "is_active": True,
            }
        }


class JobUpdateSchema(BaseModel):
    """Shema to update model"""

    id: int
    title: Optional[str]
    discription: Optional[str]
    salary_from: int = 0
    salary_to: int = 0
    is_active: Optional[bool]

    _salary_validation_ = root_validator(allow_reuse=True)(salary_match)

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "title": "Povar",
                "discription": "Salat rezat",
                "salary_from": 0,
                "salary_to": 10,
                "is_active": True,
            }
        }
