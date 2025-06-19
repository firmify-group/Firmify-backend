from fastapi import APIRouter, HTTPException
from src.models.request_models.object_request_in import ObjectRequestIn
from src.models.response_models.object_request_out import ObjectRequestOut
from src.service.object_request_service import object_request_service

router = APIRouter()

@router.patch("/api/office/request/object", response_model=ObjectRequestOut)
async def object_request(body: ObjectRequestIn):
    success = await object_request_service(body.id, body.description)
    if not success:
        raise HTTPException(status_code=400, detail="Solo pueden objetarse solicitudes RECHAZADAS")

    return {"message": "Se ha objetado la solicitud"}
