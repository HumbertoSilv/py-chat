from pydantic import BaseModel


class AccessToken(BaseModel):
    token_type: str = 'bearer'
    access_token: str
