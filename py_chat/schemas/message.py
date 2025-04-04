from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class MessagePublic(BaseModel):
    id: UUID
    content: str
    created_at: datetime
    updated_at: datetime


class MessageSchema(BaseModel):
    user_id: UUID
    chat_id: UUID
    content: str
