from supabase import create_client, Client
from config import settings
from src.models.request_model import RequestOut
from datetime import datetime
supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)


async def get_all_requests() -> list[RequestOut]:
    response = (
        supabase
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

        result.append(RequestOut(
            id=item.get("id"),
            rut=user.get("rut", ""),
            email=user.get("email", ""),
            name=user.get("name", ""),
            category=category.get("category_name") if category else None,
            status=state.get("state_name") if state else None,
            start_date=start_date,
            end_date=end_date
        ))

    print(result)
    return result