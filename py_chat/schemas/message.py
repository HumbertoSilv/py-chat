from uuid import UUID

from pydantic import BaseModel


class MessagePublic(BaseModel):
    id: UUID
    content: str


class MessageSchema(BaseModel):
    user_id: UUID
    chat_id: UUID
    content: str
