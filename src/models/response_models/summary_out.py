from pydantic import BaseModel
import datetime

class RequestSummary(BaseModel):
    totalResueltos: int
    totalPendientes: int
    totalObjeciones: int
    totalProcesos: int

class CategorySummary(BaseModel):
    name: str
    total: int

class SummaryDataOut(BaseModel):
    request: RequestSummary
    categorySummaries: CategorySummary[]

class SummaryOut(BaseModel):
    status: bool
    timestamp: datetime
    message: str
    data: SummaryDataOut
