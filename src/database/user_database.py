from ..database.deps import super_client
from ..models.request_models.user_in import UserRequest, UserSave



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
        "rol_id": 1
    }).execute()

    print("Employee created:", employee.data)
    return employee.data

def get_employee_by_email(email: str):
    employee = super_client.table("user").select("*").eq("email", email).execute()
    
    if employee.data:
        return employee.data[0]
    else:
        return None
    
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