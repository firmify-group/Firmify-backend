from supabase import create_client, Client
from config import settings

supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

async def evaluate_request_service(request_id: int, new_status: str) -> bool:
    try:
        state_response = supabase.table("state").select("id").eq("state_name", new_status.upper()).execute()
        state_data = state_response.data

        if not state_data:
            print(f"Estado no encontrado: {new_status}")
            return False

        new_state_id = state_data[0]["id"]

        update_response = supabase.table("request").update({"state_id": new_state_id}).eq("id", request_id).execute()

        return len(update_response.data) > 0

    except Exception as e:
        print(f"Error al evaluar la solicitud: {e}")
        return False
