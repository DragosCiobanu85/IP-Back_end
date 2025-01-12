# dto/status.py
from pydantic import BaseModel

class StatusBase(BaseModel):
    nume: str

    class Config:
        orm_mode = True

class StatusCreate(StatusBase):
    pass

class StatusUpdate(StatusBase):
    pass

class StatusResponse(StatusBase):
    id_Status: int

    class Config:
        orm_mode = True
