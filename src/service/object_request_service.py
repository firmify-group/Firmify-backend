from supabase import create_client, Client
from config import settings

supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

async def object_request_service(request_id: int, description: str) -> bool:
    try:
        request_check = supabase.table("request")\
            .select("id, state_id")\
            .eq("id", request_id)\
            .single()\
            .execute()

        request_data = request_check.data
        if not request_data:
            return False

        if request_data["state_id"] != 5:
            return False

        insert_response = supabase.table("objection").insert({
            "description": description,
            "request_id": request_id,
            "state_id": 2
        }).execute()

        if not insert_response.data:
            return False

        update_response = supabase.table("request").update({
            "state_id": 2
        }).eq("id", request_id).execute()

        if not update_response.data:
            return False

        return True

    except Exception as e:
        print("Error en object_request_service:", e)
        return False
