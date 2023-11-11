from pydantic import BaseModel

from schema.schemaShop import Shop
from schema.schemaCategory import Category


class ShopCategoryBase(BaseModel):
    shop_id: int
    category_id: int


class ShopCategoryCreate(ShopCategoryBase):
    pass


class ShopCategoryPatch(BaseModel):
    pass


class ShopCategory(Shop):
    category: list[Category]

    class Congig:
        orm_mode = True


class CategoryShop(Category):
    shop: list[Shop]

    class Congig:
        orm_mode = True
