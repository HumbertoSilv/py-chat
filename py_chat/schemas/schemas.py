from typing import List
from uuid import UUID
from pydantic import BaseModel, EmailStr

from py_chat.models.user import ChatType


class UserId(BaseModel):
    id: UUID


class UserPublic(BaseModel):
    username: str
    email: EmailStr
    name: str | None
    avatar_url: str | None


class UserSchema(BaseModel):
    username: str
    email: EmailStr


class FriendList(BaseModel):
    friends: List[UserPublic]


class CreateDirectChatSchema(BaseModel):
    destination_user_id: UUID


class PublicDirectChatSchema(BaseModel):
    id: UUID


class ReceiveMessageSchema(BaseModel):
    user_id: UUID
    chat_id: UUID
    content: str


class MessageSchema(BaseModel):
    id: UUID
    content: str


class ChatSchema(BaseModel):
    id: UUID
    chat_type: ChatType
    users: List[UserPublic]
    messages: List[MessageSchema]

    class Config:
        from_attributes = True  # Permite converter diretamente de SQLAlchemy
