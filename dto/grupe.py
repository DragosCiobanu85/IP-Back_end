from pydantic import BaseModel,StringConstraints
from typing import Optional,Annotated

class GrupaBase(BaseModel):
    nume: Annotated[str, StringConstraints(pattern=r"^\d{4}$")]
    facultate_id: int

class GrupaCreate(GrupaBase):
    pass

class GrupaUpdate(BaseModel):
    nume: Optional[Annotated[str, StringConstraints(pattern=r"^\d{4}$")]]
    facultate_id: Optional[int]

class GrupaResponse(GrupaBase):
    id_Grupa: int

    class Config:
        from_attributes = True
