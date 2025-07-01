import asyncio
from datetime import datetime, timezone
from typing import Optional

from fastapi import (
    APIRouter,
    File,
    Form,
    UploadFile,
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
from src.models.request_models.request_in import RequestSave
from src.models.response_models.categories_out import CategoryData, CategoryResponse
from src.models.request_models.requests_in import ObjectRequestIn
from src.models.response_models.requests_out import (
    GetAllRequestsOut, GetRequestsOut, ObjectRequestOut, RequestsData, RequestsOut, adminRequestOut)
from src.utils.getCurrentUser import get_current_user
from src.utils.serialize import serialize_process
from src.database.request_database import (
     create_request,
     create_request_with_upload,
     get_all_requests_admin,
     get_categories_from_db,
     getRequestsByUser,
     evaluate_request,
     object_request,
     
     )

requests_router = APIRouter()

# Crear solicitud con archivo
@requests_router.post("/api/office/request/create")
async def create_user_request(
    start_date: str = Form(...),
    end_date: str = Form(...),
    category_id: int = Form(...),
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    print("current_user:", current_user)
    try:
        contents = await file.read()

        result = create_request_with_upload(
            request_file=contents,
            filename=file.filename,
            content_type=file.content_type
        )

        current_user_id = current_user.get("id")
        print("id : ", current_user_id)
        result2 = create_request(start_date,end_date, category_id, current_user_id,result)

        return {
            "status": True,
            "message": "Solicitud creada exitosamente",
            "timestamp": datetime.now(timezone.utc).isoformat(timespec='minutes'),
            "data archivo": result,
            "data solicitud": result2
        }

    except Exception as e:
        print("Error al crear solicitud:", e)
        raise HTTPException(status_code=500, detail="Error interno del servidor")
    


# Crear solicitud
@requests_router.post("/api/office/request/create2")
async def create_user_request(
    start_date: str = Form(...),
    end_date: str = Form(...),
    category_id: int = Form(...),
    current_user: dict = Depends(get_current_user)
):
    print("current_user:", current_user)
    try:
           
        result = create_request(start_date,end_date, category_id, current_user.get(id))

        return {
            "status": True,
            "message": "Solicitud creada exitosamente",
            "timestamp": datetime.now(timezone.utc).isoformat(timespec='minutes'),
            "data": result
        }

    except Exception as e:
        print("Error al crear solicitud:", e)
        raise HTTPException(status_code=500, detail="Error interno del servidor")


# Evaluar solicitud
@requests_router.post("/api/manager/request/valuate", response_model=ObjectRequestOut)
async def valuate_request(id: int = Query(), status: str = Query()):
        success = await evaluate_request(id, status)
        if not success:
            raise HTTPException(
                status_code=400, detail="No se pudo actualizar la solicitud")
        return ObjectRequestOut(message=f"Solicitud {status.lower()}".capitalize())

# Obtener todos los procesos para dashboard
@requests_router.get("/api/manager/process", response_model=GetRequestsOut)
async def get_all_requests(current_user: dict = Depends(get_current_user)):
    try:
        if current_user.get("role") != "SUPERVISOR":
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


        
@requests_router.get("/api/office/request/all", response_model=GetAllRequestsOut)
async def fetch_requests(current_user: dict = Depends(get_current_user)):
    try:
        user_id = current_user["id"]
        processes = getRequestsByUser(user_id)

        serialized = [serialize_process(p) for p in processes]
        data = RequestsData(request=serialized)

        message = "No hay solicitudes registradas" if not serialized else "Solicitud aceptada"

        return GetAllRequestsOut(
        status=True,
        timestamp=datetime.now(timezone.utc).time().isoformat(timespec='minutes'),
        message=message,
        data={"request": serialized}
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


# Obtener categorías
@requests_router.get("/api/categories", response_model=CategoryResponse)
async def get_categories(current_user: dict = Depends(get_current_user)):
    try:
        if current_user.get("role") not in ["SUPERVISOR", "USER"]:
            raise HTTPException(status_code=403, detail="Acceso no autorizado")
        
        categories = get_categories_from_db()
        print(categories)
        return CategoryResponse(data=CategoryData(categories=categories))

    except HTTPException:
        raise
    except Exception as e:
        print("Error en get_categories endpoint:", e)
        raise HTTPException(status_code=500, detail="Error interno del servidor")