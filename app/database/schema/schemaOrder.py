from datetime import datetime

from pydantic import BaseModel

from schema.schemaContact import Contact
from schema.schemaShoppingCart import ShoppingCart


class OrderBase(BaseModel):
    contact_id: int
    shoppingCart_id: int


class OrderCreate(OrderBase):
    pass


class OrderPatch(BaseModel):
    pass


class Order(OrderBase):
    id: int 
    created_at: datetime
    update_at: datetime
    contact: Contact
    shoppingCart: ShoppingCart

    class Congig:
        orm_mode = True