from pydantic import BaseModel
from datetime import datetime

class RequestSave(BaseModel):
    start_date: datetime
    end_date: datetime
    category_id: int
