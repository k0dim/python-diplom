from typing import Optional, Union, Literal

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    lastname: str
    firstname: str
    surename: Union[str, None]
    type: Literal['shop', 'buyer']
    email: EmailStr
    company: str
    position: Union[str, None]

    class Congig:
        orm_mode = True

class UserCreate(UserBase):
    password: str


class UserPatch(BaseModel):
    lastname: str | None = None
    firstname: str | None = None
    surename: Union[str, None] | None = None
    type: Literal['shop', 'buyer'] | None = None
    email: EmailStr | None =  None
    company: str | None = None
    position: Union[str, None] | None = None

    class Congig:
        orm_mode = True


class User(UserBase):
    id: int