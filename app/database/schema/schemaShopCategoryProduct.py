from typing import Optional, Union

from pydantic import BaseModel

from schema.schemaShop import ShopCreate, Shop
from schema.schemaCategory import CategoryCreate, Category
from schema.schemaProductInfo import ProductInfoCreate, ProductInfo


class ShopCategoryProductBase(BaseModel):
    shop: ShopCreate
    categories: list[CategoryCreate]
    goods: list[ProductInfoCreate]


class ShopCategoryProductCreate(ShopCategoryProductBase):
    pass


class ShopCategoryProductPatch(BaseModel):
    pass


class ShopCategoryProduct(ShopCategoryProductBase):
    shop: Shop
    categories: list[Category]
    goods: list[ProductInfo]

    class Congig:
        orm_mode = True