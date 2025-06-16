from pydantic import BaseModel

class RequestOut(BaseModel):
    id: int
    category_name: str
    state_name: str
