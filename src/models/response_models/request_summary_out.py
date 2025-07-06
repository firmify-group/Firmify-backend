from typing import List
from pydantic import BaseModel
from datetime import datetime


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
    categorySumers: List[RequestCategorySummary]

class RequestSummaryOut(BaseModel):
    status: bool
    timestamp: datetime
    message: str
    data: RequestSummaryDataOut