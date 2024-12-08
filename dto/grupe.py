from pydantic import BaseModel,StringConstraints
from typing import Optional,Annotated

class GrupaBase(BaseModel):
    nume: Annotated[str, StringConstraints(pattern=r"^\d{4}$")]
    id_Facultate: int

class GrupaCreate(GrupaBase):
    pass

class GrupaUpdate(BaseModel):
    nume: Optional[Annotated[str, StringConstraints(pattern=r"^\d{4}$")]]
    id_Facultate: Optional[int]

class GrupaResponse(GrupaBase):
    
    id_Grupa: int

    class Config:
        from_attributes = True
