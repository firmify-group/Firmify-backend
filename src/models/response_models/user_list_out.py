from datetime import datetime
from typing import List
from pydantic import BaseModel

class UserListDataOut(BaseModel):
    id: str
    name: str
    rut: str
    email: str

class UserListDataWrapper(BaseModel):
    users: List[UserListDataOut]

class UserListOut(BaseModel):
    status: bool
    message: str
    timestamp: datetime
    data: UserListDataWrapper
