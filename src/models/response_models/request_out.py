from pydantic import BaseModel
import datetime

class RequestDataOut(BaseModel):
    id: int
    category: str
    state: str

class RequestOut(BaseModel):
    status: bool
    timestamp: datetime
    message: str
    data: RequestDataOut[]
