from pydantic import BaseModel
from typing import Optional

class GrupaBase(BaseModel):
    nume: str
    facultate_id: int

class GrupaCreate(GrupaBase):
    pass

class GrupaUpdate(BaseModel):
    nume: Optional[str]
    facultate_id: Optional[int]

class GrupaResponse(GrupaBase):
    id_Grupa: int

    class Config:
        from_attributes = True
