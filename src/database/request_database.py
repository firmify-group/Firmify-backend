from ..database.deps import super_client
from ..models.request_models.request_in import RequestRequest, RequestSave
from ..service import auth_service
from src.models.response_models.requests_out import adminRequestOut
from fastapi import HTTPException
from datetime import datetime
from typing import Optional


# Crear solicitud
def create_request(request: RequestSave):
    try:
        response = super_client.table("request").insert({
            "start_date": datetime.now(),
            "end_date": request.end_date,
            "file": request.file,
            "category_id": request.category_id,
            "user_id": auth_service.get_user_id(),
        }).execute()
        return response.data
    except Exception as e:
        print(f"Error al crear solicitud: {e}")
        return None


# Obtener solicitudes dentro de un intervalo de fechas
def get_request_from_date_intervals(from_date: datetime, until_date: datetime):
    try:
        response = (
            super_client
            .table("request")
            .select("start_date")
            .range_gte("start_date", [from_date, until_date])
            .execute()
        )
        return response.data or None
    except Exception as e:
        print(f"Error al obtener solicitudes por fecha: {e}")
        return None


# Obtener solicitudes por ID de usuario
def get_request_by_user_id(user_id):
    try:
        response = (
            super_client
            .table("request")
            .select("*")
            .eq("user_id", user_id)
            .execute()
        )
        return response.data or None
    except Exception as e:
        print(f"Error al obtener solicitudes por usuario: {e}")
        return None


# Obtener todas las solicitudes (versión básica)
def get_all_request():
    try:
        response = (
            super_client
            .table("request")
            .select("*")
            .execute()
        )
        return response.data or None
    except Exception as e:
        print(f"Error al obtener todas las solicitudes: {e}")
        return None


# Obtener todas las solicitudes (versión administrador)
async def get_all_requests_admin() -> list[adminRequestOut]:
    try:
        response = (
            super_client
            .from_("request")
            .select("""
                id,
                start_date,
                end_date,
                user: user_id ( rut, email, name ),
                category: category_id (category_name),
                state: state_id (state_name)
            """)
            .execute()
        )

        data = response.data or []
        result = []

        for item in data:
            user = item.get("user") or {}
            category = item.get("category")
            state = item.get("state")

            start_date_raw = item.get("start_date")
            end_date_raw = item.get("end_date")

            start_date = datetime.fromisoformat(start_date_raw).date() if isinstance(start_date_raw, str) else start_date_raw
            end_date = datetime.fromisoformat(end_date_raw).date() if isinstance(end_date_raw, str) else end_date_raw

            result.append(adminRequestOut(
                id=item.get("id"),
                rut=user.get("rut", ""),
                email=user.get("email", ""),
                name=user.get("name", ""),
                category=category.get("category_name") if category else None,
                status=state.get("state_name") if state else None,
                start_date=start_date,
                end_date=end_date
            ))

        return result

    except Exception as e:
        print(f"Error en get_all_requests_admin: {e}")
        return []


# Obtener solicitudes creadas por el usuario actual
def getRequestsByUser(user_id: Optional[str] = None):
    try:
        query = (
            super_client.table("request")
            .select("id, category:category_id(category_name), state:state_id(state_name)")
        )
        if user_id:
            query = query.eq("user_id", user_id)

        response = query.execute()
        return response.data or []

    except Exception as e:
        print(f"Error en getRequestsByUser: {e}")
        return []


# Objetar una solicitud
async def object_request(request_id: int, description: str) -> bool:
    try:
        request_check = (
            super_client.table("request")
            .select("id, state_id")
            .eq("id", request_id)
            .single()
            .execute()
        )

        request_data = request_check.data
        if not request_data or request_data["state_id"] != 5:
            return False

        insert_response = super_client.table("objection").insert({
            "description": description,
            "request_id": request_id,
            "state_id": 2
        }).execute()

        if not insert_response.data:
            return False

        update_response = super_client.table("request").update({
            "state_id": 2
        }).eq("id", request_id).execute()

        return bool(update_response.data)

    except Exception as e:
        print(f"Error en object_request: {e}")
        return False


# Evaluar (cambiar estado de) una solicitud
async def evaluate_request(request_id: int, new_status: str) -> bool:
    try:
        state_response = super_client.table("state").select("id").eq("state_name", new_status.upper()).execute()
        state_data = state_response.data

        if not state_data:
            print(f"Estado no encontrado: {new_status}")
            return False

        new_state_id = state_data[0]["id"]

        update_response = super_client.table("request").update({"state_id": new_state_id}).eq("id", request_id).execute()

        return len(update_response.data) > 0

    except Exception as e:
        print(f"Error en evaluate_request: {e}")
        return False
