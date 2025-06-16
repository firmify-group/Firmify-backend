from pydantic import BaseModel
import datetime

class RequestSave(BaseModel):
    start_date: datetime
    end_date: datetime
    file: str
    category_id: int
