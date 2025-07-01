from pydantic import BaseModel, field_validator
from typing import List, Any
from pydantic import BaseModel
from datetime import date, datetime

class RequestItem(BaseModel):
    id: int
    category: str
    state: str
    created_at: date
    finished_at: date

class RequestsData(BaseModel):
    request: List[RequestItem]

class GetRequestsOutData(BaseModel):
    request: List[RequestItem]

class RequestsOut(BaseModel):
    status: bool
    message: str
    timestamp: str
    data: List[RequestsData]

class GetAllRequestsOut(BaseModel):
    status: bool
    timestamp: str
    message: str
    data: RequestsData

class ObjectRequestOut(BaseModel):
    message: str

class adminRequestOut(BaseModel):
    id: int
    rut: str
    email: str
    name: str
    category: str
    status: str
    start_date: date
    end_date: date

class GetRequestsOut(BaseModel):
    status: bool
    message: str
    timestamp: str
    data: List[adminRequestOut]

    @field_validator('status', mode='before')
    @classmethod
    def lower_status(cls, v):
        if isinstance(v, str):
            return v.lower()
        return v

    class Config:
        json_encoders = {
            date: lambda v: v.strftime('%Y-%m-%d') if v else None,
            datetime: lambda v: v.strftime('%Y-%m-%d') if v else None
        }