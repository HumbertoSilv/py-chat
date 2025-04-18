from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class UserId(BaseModel):
    id: UUID


class UserPublic(BaseModel):
    username: str
    email: EmailStr
    name: str | None
    avatar_url: str | None

    model_config = ConfigDict(from_attributes=True)


class CreateUserSchema(BaseModel):
    username: str
    email: EmailStr


class UpdateUserSchema(BaseModel):
    name: str | None = None
    avatar_url: str | None = None


class UserQuery(BaseModel):
    username: str
