from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from jwt import encode

from py_chat.core.config import Settings

settings = Settings()


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRES_MINUTES
    )

    to_encode.update({'exp': expire})
    encoded_jwt = encode(
        to_encode,
        settings.SECRET_KEY,
        settings.ALGORITHM,
    )

    return encoded_jwt
