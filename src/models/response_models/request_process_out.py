from pydantic import BaseModel
import datetime

class RequestProcessDataOut(BaseModel):
    id: int
    rut: str
    email: str
    name: str
    category: str
    status: str
    start_date: datetime
    end_date: datetime
    
class RequestProcessOut(BaseModel):
    status: bool
    timestamp: datetime
    message: str
    data: RequestProcessDataOut[]
