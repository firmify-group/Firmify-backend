def serialize_process(p: dict) -> dict:
    return {
        "id": p["id"],
        "category": p["category"]["category_name"],
        "state": p["state"]["state_name"]
    }

