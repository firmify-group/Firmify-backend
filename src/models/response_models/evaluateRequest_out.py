from pydantic import BaseModel

class EvaluateRequestOut(BaseModel):
    message: str
