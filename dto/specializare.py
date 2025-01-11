from pydantic import BaseModel
from typing import Optional

# DTO pentru crearea unei specializări
class SpecializareCreate(BaseModel):
    nume: str
    id_Facultate: int

# DTO pentru actualizarea unei specializări
class SpecializareUpdate(BaseModel):
    nume: Optional[str] = None
    id_Facultate: Optional[int] = None

# DTO pentru răspunsul unui endpoint
class SpecializareResponse(BaseModel):
    id_Specializare: int
    nume: str
    id_Facultate: int

    class Config:
        from_attributes = True
