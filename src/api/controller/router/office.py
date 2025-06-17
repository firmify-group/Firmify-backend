import asyncio
from datetime import datetime, timezone
from fastapi import (
    APIRouter,
    Request,
    HTTPException,
    Query,
    Depends,
    status,
)
from src.models.response_models.getRequests_model import GetRequestsOut
from src.service.getRequests_service import getRequests_service
from src.api.controller.getCurrentUser import get_current_user
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from typing import Optional
from config import settings

router = APIRouter()

#Endpoint obtener solicitudes
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = settings.JWT_SECRET_KEY
ALGORITHM = settings.JWT_ALGORITHM

def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: Optional[int] = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        return user_id
    except JWTError:
        raise credentials_exception

@router.get("/api/office/request/all", response_model=GetRequestsOut)
def get_office_requests(current_user: dict = Depends(get_current_user)):
    try:
        user_id = current_user["id"]
        raw_data = getRequests_service(user_id=user_id)

        return {
            "status": "success",
            "timestamp": datetime.now(timezone.utc).time().isoformat(timespec='minutes'),
            "message": "Solicitudes obtenidas",
            "data": raw_data or []
        }

    except HTTPException:
        raise
    except Exception as e:
        print("Error en get_office_requests:", e)
        raise HTTPException(status_code=500, detail="Error interno del servidor")
