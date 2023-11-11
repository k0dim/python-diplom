from typing import Optional, Union

from pydantic import BaseModel

from schema.chemaShopping import Shopping


class ShoppingCartBase(BaseModel):
    user_id: int


class ShoppingCartCreate(ShoppingCartBase):
    pass


class ShoppingCartPatch(BaseModel):
    pass


class ShoppingCart(ShoppingCartBase):
    id: int
    shopping: list[Shopping]
    
    class Congig:
        orm_mode = True