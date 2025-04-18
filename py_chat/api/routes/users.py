from http import HTTPStatus
from typing import Annotated, List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from py_chat.api.dependencies import get_current_user, get_user_repository
from py_chat.core.database import get_async_session
from py_chat.core.logger import logger
from py_chat.models.repositories.interfaces.user import UserRepositoryInterface
from py_chat.models.user import User
from py_chat.schemas.user import (
    CreateUserSchema,
    UserId,
    UserPublic,
    UserQuery,
)
from py_chat.service.user import create_user, search_users_by_username

router = APIRouter(prefix='/users', tags=['Users'])

T_Session = Annotated[AsyncSession, Depends(get_async_session)]
T_Repository = Annotated[UserRepositoryInterface, Depends(get_user_repository)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]
T_Query = Annotated[UserQuery, Query()]


@router.post('/create', status_code=HTTPStatus.CREATED, response_model=UserId)
async def create_new_user(
    user_repository: T_Repository, payload: CreateUserSchema
):
    logger.debug('Create user request: {}', payload)

    new_user = await create_user(user_repository, payload)

    return UserId(id=new_user.id)


@router.get('/profile', status_code=HTTPStatus.OK, response_model=UserPublic)
async def get_user_profile(current_user: T_CurrentUser):
    logger.debug('Get user profile request: {}', current_user.id)

    return current_user


@router.get(
    '/search', status_code=HTTPStatus.OK, response_model=List[UserPublic]
)
async def search_for_profile(user_repository: T_Repository, query: T_Query):
    logger.debug('Search user by username request: {}', query.username)

    list_of_users = await search_users_by_username(
        user_repository, query.username
    )

    return list_of_users
