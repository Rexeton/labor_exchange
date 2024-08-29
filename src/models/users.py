from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: str
    email: str
    name: str
    is_company: bool
