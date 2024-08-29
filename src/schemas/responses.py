"""Module of schemas of responses"""

import datetime

from pydantic import BaseModel


class ResponsesSchema(BaseModel):
    """Shema of model"""

    id: int
    user_id: int
    job_id: int
    message: str
    created_at: datetime.datetime

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "user_id": 2,
                "job_id": 1,
                "message": "well_done",
                "created_at": "2024-08-06T20:41:48.521Z",
            }
        }


class ResponsesCreateSchema(BaseModel):
    """Schema to create"""

    job_id: int
    message: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "job_id": 1,
                "message": "well_done",
            }
        }


class ResponsesUpdateSchema(BaseModel):
    """schema to patch"""

    id: int
    message: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "message": "very_well_done",
            }
        }
