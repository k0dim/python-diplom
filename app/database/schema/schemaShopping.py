from typing import Optional, Union

from pydantic import BaseModel

from schema.schemaProductInfo import ProductInfo


class ShoppingBase(BaseModel):
    shoppingCart_id: int
    quntity: int


class ShoppingCreate(ShoppingBase):
    productInfo_id: int


class ShoppingPatch(BaseModel):
    productInfo_id: Optional[int]
    quntity: Optional[int]


class Shopping(ShoppingBase):
    id: int
    productInfo: ProductInfo
    
    class Congig:
        orm_mode = True