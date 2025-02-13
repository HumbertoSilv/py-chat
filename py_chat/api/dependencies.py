from typing import Annotated

from fastapi import Header


def get_current_user(user_id: str | None = Header(default=None)):
    return user_id
