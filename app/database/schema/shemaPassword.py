from pydantic import BaseModel


class PasswordBase(BaseModel):
    user_id: int
    password: str


class PasswordCreate(PasswordBase):
    pass


class PasswordPatch(BaseModel):
    pass


class Password(PasswordBase):
    id: int

    class Congig:
        orm_mode = True

