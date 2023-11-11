from datetime import datetime

from pydantic import BaseModel, EmailStr


class TokenBase(BaseModel):
    pass

    class Congig:
        orm_mode = True


class TokenCreate(TokenBase):
    email: EmailStr
    password: str


class TokenPatch(BaseModel):
    pass


class Token(TokenBase):
    access_token: str
    token_type: str

