from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel

from py_chat.models.user import ChatType
from py_chat.schemas.message import MessagePublic
from py_chat.schemas.user import UserPublic


class ChatId(BaseModel):
    id: UUID


class ChatSchema(BaseModel):
    destination_user_id: UUID


class ChatPublic(BaseModel):
    id: UUID
    chat_type: ChatType
    last_message: Optional[MessagePublic]
    users: List[UserPublic]

    class Config:
        from_attributes = True  # Permite converter diretamente de SQLAlchemy
