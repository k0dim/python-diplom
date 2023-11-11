from typing import Optional, Union

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    lastname: str
    firstname: str
    surename: Union[str, None]
    type: str
    email: EmailStr
    company: str
    position: Union[str, None]


class UserCreate(UserBase):
    password: str


class UserPatch(BaseModel):
    lastname: Optional[str]
    firstname: Optional[str]
    surename: Optional[Union[str, None]]
    type: Optional[str]
    email: Optional[EmailStr]
    company: Optional[str]
    position: Optional[Union[str, None]]
    password: Optional[Union[str, None]]


class User(UserBase):
    id: int

    class Congig:
        orm_mode = True