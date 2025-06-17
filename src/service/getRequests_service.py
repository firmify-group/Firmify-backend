from typing import Optional
from supabase import create_client, Client
from config import settings

supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

def getRequests_service(user_id: Optional[str] = None):
    try:
        query = (
            supabase.table("request")
            .select("id, category:category_id(category_name), state:state_id(state_name)")
        )
        if user_id:
            query = query.eq("user_id", user_id)

        response = query.execute()
        print(response.data)
        return response.data or []

    except Exception as e:
        print(f"Error en get_requests_service: {e}")
        return []

