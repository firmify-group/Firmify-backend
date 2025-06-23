import asyncio
from datetime import datetime, timezone
from typing import Optional

from fastapi import (
    APIRouter,
    WebSocket,
    WebSocketDisconnect,
    HTTPException,
    Query,
    Depends,
    status,
)

from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from config import settings
from src.models.request_models.requests_in import ObjectRequestIn
from src.models.response_models.requests_out import (
    GetAllRequestsOut, ObjectRequestOut, RequestsOut, adminRequestOut)
from src.utils.getCurrentUser import get_current_user
from src.utils.serialize import serialize_process
from src.database.request_database import (
     get_all_requests_admin,
     getRequestsByUser,
     evaluate_request,
     object_request,
     
     )

requests_router = APIRouter()

# Evaluar solicitud
@requests_router.post("/api/manager/request/valuate", response_model=ObjectRequestOut)
async def valuate_request(id: int = Query(), status: str = Query()):
        success = await evaluate_request(id, status)
        if not success:
            raise HTTPException(
                status_code=400, detail="No se pudo actualizar la solicitud")
        return ObjectRequestOut(message=f"Solicitud {status.lower()}".capitalize())

# Obtener todos los procesos para dashboard
@requests_router.get("/api/manager/process", response_model=GetAllRequestsOut)
async def get_all_requests(current_user: dict = Depends(get_current_user)):
    try:
        if current_user.get("rol") != "SUPERVISOR":
            raise HTTPException(status_code=403, detail="Acceso restringido a funcionarios")

        user_id = current_user["id"]
        raw_data = await get_all_requests_admin()

        return {
            "status": True,
            "timestamp": datetime.now(timezone.utc).time().isoformat(timespec='minutes'),
            "message": "Solicitud aceptada",
            "data": raw_data or []
        }

    except HTTPException:
        raise
    except Exception as e:
        print("Error en get_office_requests:", e)
        raise HTTPException(status_code=500, detail="Error interno del servidor")


#WebSocket para obtener solicitudes (cada 5 segundos)
@requests_router.websocket("/ws/manager/process")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            processes = await get_all_requests_admin()
            await websocket.send_json({
                "processes": [serialize_process(p) for p in processes]
            })
            await asyncio.sleep(5)
    except WebSocketDisconnect:
        pass
    except Exception:
        pass


        
# Obtener solicitudes del usuario actual   
@requests_router.get("/api/office/request/all", response_model=GetAllRequestsOut)
async def fetch_requests(current_user: dict = Depends(get_current_user)):
    try:
        user_id = current_user["id"]
        processes = getRequestsByUser(user_id)

        serialized = [serialize_process(p) for p in processes]

        message = "No hay solicitudes registradas" if not serialized else "Solicitud aceptada"

        return GetAllRequestsOut(
            status=True,
            timestamp=datetime.now(timezone.utc).time().isoformat(timespec='minutes'),
            message=message,
            data=serialized
        )

    except Exception as e:
        print("Error en fetch_requests:", e)
        raise HTTPException(status_code=500, detail="Error interno del servidor")


# Objetar solicitud
@requests_router.patch("/api/office/request/object", response_model=ObjectRequestOut)
async def object_request_endpoint(body: ObjectRequestIn):
        success = await object_request(body.id, body.description)
        if not success:
            raise HTTPException(
                status_code=400, detail="Solo pueden objetarse solicitudes RECHAZADAS")
        return {"message": "Se ha objetado la solicitud"}

