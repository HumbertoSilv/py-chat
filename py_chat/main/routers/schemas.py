from pydantic import BaseModel, EmailStr


class UserPublic(BaseModel):
    id: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
