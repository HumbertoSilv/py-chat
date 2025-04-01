from http import HTTPStatus
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from py_chat.api.dependencies import get_current_user
from py_chat.core.database import get_async_session
from py_chat.models.user import User
from py_chat.schemas.user import UserId, UserPublic, UserQuery, UserSchema

router = APIRouter(prefix='/users', tags=['Users'])

T_Session = Annotated[AsyncSession, Depends(get_async_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]
T_Query = Annotated[UserQuery, Query()]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserId)
async def create_user(user: UserSchema, session: T_Session):
    stmt = select(User).where(
        (User.username == user.username) | (User.email == user.email)
    )
    result = await session.execute(stmt)
    db_user = result.scalars().first()

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Username already exists',
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Email already exists',
            )

    db_user = User(**user.model_dump())

    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)

    return UserId(id=str(db_user.id))


@router.get('/profile', status_code=HTTPStatus.OK, response_model=UserPublic)
async def get_user_profile(current_user: T_CurrentUser):
    return current_user


@router.get(
    '/search', status_code=HTTPStatus.OK, response_model=List[UserPublic]
)
async def get_user_profile(session: T_Session, query: T_Query):
    stmt = select(User).where(User.username.like(f'%{query.username}%'))

    result = await session.execute(stmt)
    users = result.scalars().all()

    return users
