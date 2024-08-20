from pydantic import BaseModel


class ResponseMessage(BaseModel):
    message: str


class UserMessage(BaseModel):
    message: str


class JobMessage(BaseModel):
    message: str
