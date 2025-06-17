from pydantic import BaseModel, Field

class ObjectRequestIn(BaseModel):
    id: int
    description: str = Field(..., max_length=255)
