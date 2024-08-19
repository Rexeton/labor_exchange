from pydantic import BaseModel


class Response_message(BaseModel):
    message: str


class User_message(BaseModel):
    message: str


class Job_message(BaseModel):
    message: str
