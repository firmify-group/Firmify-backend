import asyncio
from os import stat
from fastapi import APIRouter, HTTPException
from src.database.user_database import create_employee_by_admin
from src.models.request_models.user_in import UserCreateRequest

user_router = APIRouter()

@user_router.post("/api/manager/officer/add")
async def create_employee_endpoint(employee: UserCreateRequest):
    try:
        new_employee = await asyncio.to_thread(create_employee_by_admin, employee)

        return {
            "status": True,
            "message": "Empleado creado correctamente",
            "data": new_employee
        }
    except Exception as e:
        print("ERROR INTERNO:", str(e))
        raise e
