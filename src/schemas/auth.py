from pydantic import BaseModel, BaseSettings, EmailStr, Field


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class LoginSchema(BaseModel):
    email: EmailStr
    password: str


class AuthConfiguration(BaseSettings):
    server_url: str = Field(validation_alias="SERVER_URL")
    realm: str = Field(validation_alias="REALM")
    client_id: str = Field(validation_alias="CLIENT_ID")
    client_secret: str = Field(validation_alias="CLIENT_SECRET")
    authorization_url: str = Field(validation_alias="AUTHORIZATION_URL")
    token_url: str = Field(validation_alias="TOKEN_URL")
