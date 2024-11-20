# Modelul Pydantic pentru datele Profesor
from pydantic import BaseModel

class ProfesorBase(BaseModel):
    nume: str
    prenume: str
    grad: str
    id_Facultate: int

class ProfesorCreate(ProfesorBase):
    pass

class ProfesorUpdate(BaseModel):
    nume: str
    prenume: str
    grad: str
    id_Facultate: int

class ProfesorResponse(ProfesorBase):
    id_Profesor: int

    class Config:
        orm_mode = True

