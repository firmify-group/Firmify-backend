from pydantic import BaseModel
import datetime

class RequestSummary(BaseModel):
    totalResueltos: int
    totalPendientes: int
    totalObjeciones: int
    totalProcesos: int

class RequestCategorySummary(BaseModel):
    name: str
    total: int

class RequestSummaryDataOut(BaseModel):
    request: RequestSummary
    categorySummaries: RequestCategorySummary[]

class RequestSummaryOut(BaseModel):
    status: bool
    timestamp: datetime
    message: str
    data: RequestSummaryDataOut
