from pydantic import BaseModel

class ObjectRequestOut(BaseModel):
    message: str
