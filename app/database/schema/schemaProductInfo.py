from typing import Optional, Union

from pydantic import BaseModel

from schema.schemaShop import Shop
from schema.schemaCategory import Category


class ProductInfoBase(BaseModel):
    name: str
    quntity: int
    price: float
    price_rcc: float
    model: Union[str, None]
    paramentrs: Union[dict, None]


class ProductInfoPlus(ProductInfoBase):
    shop: int
    category: int


class ProductInfoCreate(ProductInfoPlus):
    goods: list[ProductInfoPlus]



class ProductInfoPatch(BaseModel):
    name: Optional[str]
    quntity: Optional[int]
    price: Optional[float]
    price_rcc: Optional[float]
    model: Optional[str]
    paramentrs: Optional[dict]


class ProductInfo(ProductInfoBase):
    id: int
    shop: Shop
    category: Category

    class Congig:
        orm_mode = True