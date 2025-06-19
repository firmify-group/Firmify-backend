from pydantic import BaseModel
import datetime

class RequestImportDataOut(BaseModel):
    file: str
    
class RequestImportOut(BaseModel):
    status: bool
    timestamp: datetime
    message: str
    data: RequestImportDataOut
