from fastapi.security import OAuth2PasswordBearer

from config import settings as cf
from ..models.request_models.user_in import UserRequest, UserSave
from ..database import user_database
from ..models.response_models import token
from datetime import datetime, timedelta

import jwt

def create_employee(employee: UserSave) :
    employee = user_database.create_employee(employee)
    return employee

def isSupervisor(email: str):
    rol = user_database.get_rol(email)
    if not rol[0]["rol_id"]["rol_name"] == "SUPERVISOR":
        return rol
    if rol[0]["rol_id"]["rol_name"] == "SUPERVISOR":
        return True
    return False


def createToken(data: token.JWTToken, expires_in: int = 3600):
    payload = data.model_dump()
    print("payload", payload)
    #payload["exp"] = datetime.now() + timedelta(seconds=expires_in)
    token_jwt = jwt.encode(payload, cf.JWT_SECRET_KEY, algorithm="HS256")
    return token_jwt

