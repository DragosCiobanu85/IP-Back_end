# Modelul Pydantic pentru actualizarea unui student
from pydantic import BaseModel

class StudentBase(BaseModel):
    nume: str
    prenume: str
    grupa: str
    id_Facultate: int

class StudentCreate(StudentBase):
    pass

class StudentUpdate(BaseModel):
    nume: str
    prenume: str
    grupa: str
    id_Facultate: int

class StudentResponse(StudentBase):
    id_Student: int

    class Config:
        orm_mode = True
