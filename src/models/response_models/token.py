from pydantic import BaseModel

class JWTToken(BaseModel):
    id: str
    role: str 

