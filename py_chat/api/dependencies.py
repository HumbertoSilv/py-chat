from http import HTTPStatus
from uuid import UUID

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, ExpiredSignatureError, decode
from sqlalchemy.ext.asyncio import AsyncSession

from py_chat.core.config import Settings
from py_chat.core.database import get_async_session
from py_chat.models.user import User

settings = Settings()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/login')


async def get_current_user(
    session: AsyncSession = Depends(get_async_session),
    token: str = Depends(oauth2_scheme),
):
    try:
        payload = decode(
            token, settings.SECRET_KEY, algorithms=settings.ALGORITHM
        )
        user_id: str = payload.get('sub')

        if not user_id:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail='Could not validate credentials',
                headers={'WWW-Authenticate': 'Bearer'},
            )

    except DecodeError:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Signature has expired',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    user = await session.get(User, UUID(user_id))

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    return user


def decode_token(access_token: str) -> dict:
    try:
        payload = jwt.decode(
            access_token, settings.SECRET_KEY, algorithms=settings.ALGORITHM
        )
        return payload

    except jwt.ExpiredSignatureError:
        return None

    except jwt.DecodeError:
        return None
