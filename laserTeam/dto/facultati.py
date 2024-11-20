# Modelul Pydantic pentru datele Facultate
from pydantic import BaseModel

class FacultateBase(BaseModel):
    nume: str

class FacultateCreate(FacultateBase):
    pass

class FacultateResponse(FacultateBase):
    id_Facultate: int

    class Config:
        orm_mode = True