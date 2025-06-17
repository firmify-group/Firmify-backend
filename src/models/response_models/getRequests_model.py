from pydantic import BaseModel
from typing import List, Any
from pydantic import BaseModel
from datetime import datetime

class RequestItem(BaseModel):
    id: int
    category: str
    state: str

class GetRequestsOutData(BaseModel):
    request: List[RequestItem]

class GetRequestsOut(BaseModel):
    status: bool
    timestamp: str
    message: str
    data: GetRequestsOutData

class GetRequestsOut(BaseModel):
    status: str
    timestamp: str
    message: str
    data: List[Any]