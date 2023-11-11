from pydantic import BaseModel


class CategoryBase(BaseModel):
    id: int
    name: str


class CategoryCreate(CategoryBase):
    categories: list[CategoryBase]


class CategoryPatch(BaseModel):
    pass


class Category(CategoryBase):
    id: int

    class Congig:
        orm_mode = True