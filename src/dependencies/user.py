from fastapi import Depends, HTTPException, Security, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.security import keycloak_openid, oauth2_scheme
from dependencies.db import get_db
from models import User
from queries import user as user_queries


async def get_payload(token: str = Security(oauth2_scheme)) -> dict:
    try:
        return keycloak_openid.decode_token(token, validate=True)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(
    db: AsyncSession = Depends(get_db), payload: dict = Depends(get_payload)
) -> User:
    cred_exception = HTTPException(
        status_code=status.HTTP_102_PROCESSING, detail="Credentials are not valid"
    )
    try:
        print(payload)
        email = payload.get("sub")
    except Exception:
        raise cred_exception
    user = await user_queries.get_by_email(db=db, email=email)
    if user is None:
        raise cred_exception
    return user
