from fastapi import APIRouter

#from .routes import user_routes <--- ejemplo de como agregar rutas
from .router import auth_router 


api_router = APIRouter()

api_router.include_router(auth_router.router, prefix="", tags=["autentication"])