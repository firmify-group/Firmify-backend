from pydantic import BaseModel
import datetime

class ProcessDataOut(BaseModel):
    id: int
    rut: str
    email: str
    name: str
    category: str
    status: str
    start_date: datetime
    end_date: datetime
    
class ProcessOut(BaseModel):
    status: bool
    timestamp: datetime
    message: str
    data: ProcessDataOut[]
