from dateutil.parser import isoparse

def serialize_process(p: dict) -> dict:
    return {
        "id": p["id"],
        "category": p["category"]["category_name"],
        "state": p["state"]["state_name"],
        "created_at": isoparse(p["start_date"]).date() if p.get("start_date") else None,
        "finished_at": isoparse(p["end_date"]).date() if p.get("end_date") else None,
    }

