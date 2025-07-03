from pydantic import BaseModel
from typing import List

class Category(BaseModel):
    category_id: int
    category_name: str

class CategoryData(BaseModel):
    categories: List[Category]

class CategoryResponse(BaseModel):
    data: CategoryData
