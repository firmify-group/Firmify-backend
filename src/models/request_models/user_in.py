from pydantic import BaseModel


class UserRequest(BaseModel):
    full_name: str
    rut: str
    email: str

class UserSave(BaseModel):
    full_name: str
    rut: str
    email: str
    password: str
    signature: str

class UserCreateRequest(BaseModel):
    full_name: str
    rut: str
    email: str