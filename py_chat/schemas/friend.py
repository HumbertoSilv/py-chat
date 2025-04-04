from typing import List

from pydantic import BaseModel

from py_chat.schemas.user import UserPublic


class FriendListPublic(BaseModel):
    friends: List[UserPublic]
