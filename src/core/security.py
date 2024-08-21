import datetime
import os
from enum import Enum

from fastapi import HTTPException, Request, status
from fastapi.security import HTTPBearer, OAuth2AuthorizationCodeBearer
from jose import jwt
from keycloak import KeycloakOpenID
from passlib.context import CryptContext

from schemas.auth import AuthConfiguration

REFRESH_TOKEN_EXPIRE_MINUTES = int(os.environ.get("REFRESH_TOKEN_EXPIRE_MINUTES"))
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES"))
SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")

SERVER_URL = os.environ.get("SERVER_URL")
REALM = os.environ.get("REALM")
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
AUTHORIZATION_URL = os.environ.get("AUTHORIZATION_URL")
TOKEN_URL = os.environ.get("TOKEN_URL")

settings = AuthConfiguration(
    server_url=SERVER_URL,
    realm=REALM,
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    authorization_url=AUTHORIZATION_URL,
    token_url=TOKEN_URL,
)


class tokenType(Enum):
    ACCESS = "access"
    REFRESH = "refresh"


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hash: str) -> bool:
    return pwd_context.verify(password, hash)


def create_token(data: dict, token_type: str) -> str:
    time_expire = ACCESS_TOKEN_EXPIRE_MINUTES
    if token_type == tokenType.REFRESH.value:
        time_expire = REFRESH_TOKEN_EXPIRE_MINUTES

    to_encode = data.copy()
    to_encode.update({"exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=time_expire)})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str):
    try:
        encoded_jwt = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.JWSError:
        return None
    return encoded_jwt


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials = await super(JWTBearer, self).__call__(request)
        exp = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid auth token")
        if credentials:
            token = decode_access_token(credentials.credentials)
            if token is None:
                raise exp
            return credentials.credentials
        else:
            raise exp


oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=settings.authorization_url,
    tokenUrl=settings.token_url,
)

keycloak_openid = KeycloakOpenID(
    server_url=settings.server_url,
    client_id=settings.client_id,
    realm_name=settings.realm,
    client_secret_key=settings.client_secret,
    verify=True,
)
