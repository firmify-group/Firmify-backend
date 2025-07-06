import secrets
from unittest import result
from ..database.deps import super_client
from ..models.request_models.user_in import UserCreateRequest, UserRequest, UserSave
from fastapi import HTTPException

def create_employee(employee: UserSave):
    auth_user = super_client.auth.sign_up(
      { 
        "email":employee.email,
        "password": employee.password
    }

    )
    
    auth_user.user.id

    employee = super_client.table("user").insert({
        "id": auth_user.user.id,
        "rut": employee.rut,
        "name": employee.full_name,
        "email": auth_user.user.user_metadata["email"],
        "password": employee.password,
        "signature": employee.signature,
        "rol_id": 2
    }).execute()

    print("Employee created:", employee.data)
    return employee.data

def get_employee_by_email(email: str):
    employee = super_client.table("user").select("*").eq("email", email).execute()
    
    if employee.data:
        return employee.data[0]
    else:
        return None

def get_all_employee():
    response = super_client.table("user").select("*").eq("rol_id", "2").execute()
    
    if response:
        return response.data
    else:
        raise HTTPException(status_code=404, detail="No hay usuarios")

    
def get_rol(email: str):
    rol = super_client.table("user").select("rol_id!inner(rol_name)").eq("email", email).execute().data
    if rol:
        return rol[0]["rol_id"]["rol_name"]
    else:
        raise HTTPException(status_code=404, detail="Role not found for the given email")
    
    
def get_name(email: str):
    name = super_client.table("user").select("name").eq("email", email).execute().data
    
    if name:
        return name[0]["name"]
    else:
        raise HTTPException(status_code=404, detail="Name not found for the given email")
    
def delete_employee(user_id: str):
    response = super_client.table("user").delete().eq("id", user_id).execute()

    if hasattr(response, 'error') and response.error:
        raise HTTPException(status_code=400, detail=f"Error deleting user: {response.error}")
    
    return {"message": f"User {user_id} deleted successfully"}




def create_employee_by_admin(employee: UserCreateRequest):
    generated_password = secrets.token_urlsafe(12)
    default_signature = ""

    auth_user = super_client.auth.sign_up({
        "email": employee.email,
        "password": generated_password
    })

    user_id = auth_user.user.id

    result = super_client.table("user").insert({
        "id": user_id,
        "rut": employee.rut,
        "name": employee.full_name,
        "email": employee.email,
        "password": generated_password,  
        "signature": default_signature,
        "rol_id": 2
    }).execute()

    print(result)
    print(generated_password)
    error = getattr(result, "error", None)
    if error is None and hasattr(result, "_data"):
        error = result._data.get("error") if isinstance(result._data, dict) else None
    if error:
        raise Exception(f"Error creando empleado: {error}")
    return result.data
