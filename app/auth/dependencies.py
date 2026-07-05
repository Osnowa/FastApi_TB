from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.database import get_session
from app.models.users import User
from app.auth.service import decode_access_token

http_bearer = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    session: AsyncSession = Depends(get_session),
) -> User:
    token = credentials.credentials
    
    exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Невалидный токен или срок действия истёк",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_access_token(token)
    if not payload:
        raise exc

    user_id = payload.get("sub")
    if not user_id:
        raise exc

    user = await session.get(User, int(user_id))
    if not user:
        raise exc

    return user


# Псевдоним — как SessionDep, только для пользователя
CurrentUserDep = Annotated[User, Depends(get_current_user)]