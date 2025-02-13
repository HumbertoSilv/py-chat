from uuid import UUID
from pydantic import BaseModel, EmailStr


class UserId(BaseModel):
    id: str


class UserPublic(BaseModel):
    username: str
    email: EmailStr
    name: str | None
    avatar_url: str | None


class UserSchema(BaseModel):
    username: str
    email: EmailStr


class FriendList(BaseModel):
    friends: list[UserPublic]


class CreateDirectChatSchema(BaseModel):
    destination_user_id: UUID


class PublicDirectChatSchema(BaseModel):
    id: UUID
