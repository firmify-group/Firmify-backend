from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class EvaluateRequestIn(BaseModel):
    id: int
    status: str


class ObjectRequestIn(BaseModel):
    id: int
    description: str = Field(..., max_length=255)


class UserRequestIn(BaseModel):
    id: Optional[str] = None