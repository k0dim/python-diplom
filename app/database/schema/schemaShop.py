from typing import Optional, Union

from pydantic import BaseModel, HttpUrl

from schema.schemaUser import User


class ShopBase(BaseModel):
    name = str
    url = Optional[HttpUrl]
    filename = Optional[str]


class ShopCreate(ShopBase):
    pass


class ShopPatch(BaseModel):
    name = Optional[str]
    url = Optional[HttpUrl]
    filename = Optional[str]


class Shop(ShopBase):
    id: int
    is_active: bool
    url: Union[HttpUrl, None]
    filename: Union[str, None]

    class Congig:
        orm_mode = True