from pydantic import BaseModel
import datetime

class UserListDataOut(BaseModel):
    id: int
    name: str
    rut: str
    email: str

class UserListOut(BaseModel):
    status: bool
    message: str
    timestamp: datetime
    data: List[UserListDataOut]
