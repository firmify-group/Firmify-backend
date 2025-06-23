from ..database.deps import super_client
from src.models.response_models.requests_out import adminRequestOut
from datetime import datetime
from typing import Optional

#Obtener todas las solicitudes [Sólo funcionario]
async def get_all_requests_admin() -> list[adminRequestOut]:

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

        start_date = (
            datetime.fromisoformat(start_date_raw).date() if isinstance(start_date_raw, str) else start_date_raw
        )
        end_date = (
            datetime.fromisoformat(end_date_raw).date() if isinstance(end_date_raw, str) else end_date_raw
        )

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


#Obtener las solicitudes creadas por el usuario actual
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
        print(f"Error en get_requests_service: {e}")
        return []



#Objetar solicitudes
async def object_request(request_id: int, description: str) -> bool:
    try:
        request_check = super_client.table("request")\
            .select("id, state_id")\
            .eq("id", request_id)\
            .single()\
            .execute()

        request_data = request_check.data
        if not request_data:
            return False

        if request_data["state_id"] != 5:
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

        if not update_response.data:
            return False

        return True

    except Exception as e:
        print("Error en object_request_service:", e)
        return False


#Evaluar solicitudes (cambiar estado)

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
        print(f"Error al evaluar la solicitud: {e}")
        return False

