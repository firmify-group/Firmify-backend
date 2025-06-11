from pydantic import BaseModel


class UseOutData(BaseModel):
    token: str
    expires_in: int
    token_type: str



class UserAuthOut(BaseModel):
    status: bool
    data: UseOutData
    message: str

