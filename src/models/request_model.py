from pydantic import BaseModel, field_validator
from datetime import date, datetime

class RequestOut(BaseModel):
    id: int
    rut: str
    email: str
    name: str
    category: str | None = None
    status: str | None = None
    start_date: date
    end_date: date

    @field_validator('status', mode='before')
    @classmethod
    def lower_status(cls, v):
        if isinstance(v, str):
            return v.lower()
        return v

    class Config:
        json_encoders = {
            date: lambda v: v.strftime('%Y-%m-%d'),
            datetime: lambda v: v.strftime('%Y-%m-%d')
        }
