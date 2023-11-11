from datetime import datetime

from pydantic import BaseModel


class TokenBase(BaseModel):
    pass


class TokenCreate(TokenBase):
    pass


class TokenPatch(BaseModel):
    pass


class Token(TokenBase):
    token: str
    created_at: datetime

    class Congig:
        orm_mode = True

