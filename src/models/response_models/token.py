from pydantic import BaseModel

class JWTToken(BaseModel):
    id: str
    rol: str 

