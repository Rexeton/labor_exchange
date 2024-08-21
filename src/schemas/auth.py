from pydantic import BaseModel, EmailStr


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class LoginSchema(BaseModel):
    email: EmailStr
    password: str


class AuthConfiguration(BaseModel):
    server_url: str
    realm: str
    client_id: str
    client_secret: str
    authorization_url: str
    token_url: str
