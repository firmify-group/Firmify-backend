from pydantic import BaseModel
import datetime

class RequestRequest(BaseModel):
    start_date: datetime
    sign_date: datetime
    end_date: datetime
    file: str

class RequestSave(BaseModel):
    end_date: datetime
    file: str
    category_id: int
    state_id: int
