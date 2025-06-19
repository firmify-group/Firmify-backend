from pydantic import BaseModel, Field

class EvaluateRequestIn(BaseModel):
    id: int
    status: str
