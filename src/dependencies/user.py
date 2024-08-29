from fastapi import Depends, HTTPException, Security, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.security import keycloak_openid, oauth2_scheme
from dependencies.db import get_db
from models import User
from queries import user as user_queries


async def decode_token(token: str = Security(oauth2_scheme)) -> dict:
    try:
        return keycloak_openid.decode_token(token, validate=True)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )


def current_uset_is_company(role: str):
    print(role["roles"])
    print(type(["roles"]))
    if "company" in role["roles"]:
        return True
    return False


async def get_current_user(
    db: AsyncSession = Depends(get_db), payload: dict[str:str] = Depends(decode_token)
) -> User:
    cred_exception = HTTPException(
        status_code=status.HTTP_102_PROCESSING, detail="Credentials are not valid"
    )
    print(payload)
    try:
        user = User(
            id=payload.get("sub"),
            email=payload.get("email"),
            name=payload.get("preferred_username"),
            is_company=current_uset_is_company(role=payload.get("realm_access")),
        )
        print(user)
    except Exception:
        raise cred_exception
    return user
