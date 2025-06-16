from ..database.deps import super_client
from ..models.request_models.request_in import RequestRequest, RequestSave
from ..service import auth_service
import datetime

from fastapi import HTTPException

def create_request(request: RequestSave):

    request = super_client.table("request").insert({
        "start_date": datetime.datetime.now(),
        "end_date": request.end_date,
        "file": request.file,
        "category_id": request.category_id,
        "user_id": auth_service.get_user_id(),
    }).execute()

def get_request_from_date_intervals(from_date: datetime, until_date: datetime):
    request = super_client.table("request").select("start_date")
        .range_gte("start_date", [from_date, until_date]).execute()

    if request.data:
        return request.data
    else:
        return None
