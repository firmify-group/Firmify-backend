from ..database import request_database
from ..database import user_database
from src.models.response_models.requests_out import GetRequestsOut, RequestItem,ObjectRequestOut
from datetime import datetime
from typing import Optional
from src.models.response_models import user_list_out

def get_current_timestamp() -> str:
    return datetime.now().isoformat()

async def get_all_requests(email: str) -> GetRequestsOut:
    raw_data = request_database.fetch_all_requests()
    result = []

    for item in raw_data:
        category = item.get("category")
        state = item.get("state")

        result.append(RequestItem(
            id=item.get("id"),
            category=category.get("category_name") if category else "Sin categoría",
            state=state.get("state_name") if state else "Desconocido"
        ))

    return GetRequestsOut(
        status="success",
        timestamp=get_current_timestamp(),
        message="Solicitudes obtenidas correctamente",
        data=result
    )


def get_requests_by_user(user_id: Optional[str] = None) -> GetRequestsOut:
    if not user_id:
        return GetRequestsOut(
            status="error",
            timestamp=get_current_timestamp(),
            message="ID de usuario no proporcionado",
            data=[]
        )

    raw_data = request_database.fetch_requests_by_user(user_id)
    result = []

    for item in raw_data:
        category = item.get("category")
        state = item.get("state")
        result.append(RequestItem(
            id=item.get("id"),
            category=category.get("category_name") if category else "Sin categoría",
            state=state.get("state_name") if state else "Desconocido"
        ))

    return GetRequestsOut(
        status="success",
        timestamp=get_current_timestamp(),
        message="Solicitudes del usuario obtenidas correctamente",
        data=result
    )


async def object_request(request_id: int, description: str) -> ObjectRequestOut:
    request_data = request_database.get_request_by_id(request_id)

    if not request_data:
        return ObjectRequestOut(message="Solicitud no encontrada")

    if request_data["state_id"] != 5:
        return ObjectRequestOut(message="No se puede objetar. Estado inválido.")

    inserted = request_database.insert_objection(request_id, description)
    if not inserted.data:
        return ObjectRequestOut(message="Error al registrar objeción")

    updated = request_database.update_request_state(request_id, 2)
    if not updated.data:
        return ObjectRequestOut(message="Error al cambiar estado de la solicitud")

    return ObjectRequestOut(message="Solicitud objetada exitosamente")


async def evaluate_request(request_id: int, new_status: str) -> ObjectRequestOut:
    state = request_database.get_state_id_by_name(new_status)
    if not state:
        return ObjectRequestOut(message="Estado no válido")

    new_state_id = state[0]["id"]
    updated = request_database.update_request_state(request_id, new_state_id)

    if not updated.data:
        return ObjectRequestOut(message="No se pudo actualizar el estado")

    return ObjectRequestOut(message="Estado actualizado correctamente")

async def get_all_employee() -> UserListOut:
    raw_data = user_database.get_all_employee()
    result = []
    if not raw_data:
        return UserListOut(status=false,message="Error en resolver la solicitud",timestamp=get_current_timestamp(),data = [])

    for item in raw_data:
        result.append(UserListDataOut(id=item.get("id"),
            name=item.get("name"),
            rut=item.get("rut"),
            email=item.get("email")
            )
        )

    return UserListOut(status=true,message="Solicitud aceptada",timestamp=get_current_timestamp(),data=result)
