from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from py_chat.core.config import Settings
from py_chat.core.database import get_async_session
from py_chat.core.security import create_access_token
from py_chat.models.user import User
from py_chat.schemas.auth import AccessToken

router = APIRouter(prefix='/auth', tags=['auth'])

settings = Settings()
T_Session = Annotated[AsyncSession, Depends(get_async_session)]
T_OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]


# fake login for development
@router.post('/login', status_code=HTTPStatus.OK, response_model=AccessToken)
async def user_login(
    response: Response, form_data: T_OAuth2Form, session: T_Session
):
    stmt = select(User).where(User.username == form_data.username.lower())
    result = await session.execute(stmt)
    user = result.scalars().first()

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Incorrect email/username or password',
        )

    access_token = create_access_token({'sub': str(user.id)})

    response.set_cookie(
        key='access_token',
        value=access_token,
        httponly=True,  # Impede acesso via JavaScript
        secure=True,  # Precisa de HTTPS em produção
        samesite='None',  # Necessário para cross-origin em navegadores moderno
    )

    return {'access_token': access_token}
