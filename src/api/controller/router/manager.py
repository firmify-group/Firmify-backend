import asyncio
from fastapi import (
    APIRouter,
    WebSocket,
    WebSocketDisconnect,
    HTTPException,
    Query,
)
from src.models.response_models.evaluateRequest_out import EvaluateRequestOut
from src.service.evaluateRequest_service import evaluate_request_service
from src.service.request_service import get_all_requests

router = APIRouter()

#Endpoint evaluar solicitudes
@router.post("/api/manager/request/valuate", response_model=EvaluateRequestOut)
async def valuate_request(id: int = Query(), status: str = Query()):
    success = await evaluate_request_service(id, status)
    if not success:
        raise HTTPException(status_code=400, detail="No se pudo actualizar la solicitud")
    return EvaluateRequestOut(message=f"Solicitud {status.lower()}".capitalize())

#Endpoint procesos
@router.get("/api/manager/process")
async def fetch_requests():
    processes = await get_all_requests()
    return {
        "processes": [_serialize_process(p) for p in processes]
    }

#WebSocket solicitudes
@router.websocket("/ws/manager/process")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            processes = await get_all_requests()
            await websocket.send_json({
                "processes": [_serialize_process(p) for p in processes]
            })
            await asyncio.sleep(5)
    except WebSocketDisconnect:
        pass
    except Exception:
        pass

def _serialize_process(p):
    d = p.model_dump()
    if d.get("start_date"):
        d["start_date"] = d["start_date"].isoformat()
    if d.get("end_date"):
        d["end_date"] = d["end_date"].isoformat()
    return d