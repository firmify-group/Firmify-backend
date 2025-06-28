from pydantic import BaseModel
import datetime

class RequestExportDataOut(BaseModel):
    file: str
    url: str
    
class RequestExportOut(BaseModel):
    status: bool
    timestamp: datetime
    message: str
    data: RequestImportDataOut
