from pydantic import BaseModel


class PasswordBase(BaseModel):
    user_id: int
    password: str

    class Congig:
        orm_mode = True


class PasswordCreate(PasswordBase):
    pass


class PasswordPatch(BaseModel):
    password: str | None = None

    class Congig:
        orm_mode = True

        
class Password(PasswordBase):
    id: int
