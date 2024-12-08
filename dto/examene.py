from pydantic import BaseModel, conint
from datetime import time, date


# Modelul de bază pentru Examen
class ExamenBase(BaseModel):
    id_Facultate: int
    id_Profesor_1: int
    id_Materie: int
    id_Grupa: int
    data: date
    id_Sala: int
    ora: time 
    id_Cerere: int


# Model pentru crearea unui examen
class ExamenCreate(ExamenBase):
    pass


# Model pentru actualizarea unui examen
class ExamenUpdate(BaseModel):
    ora: time
    sala: str


# Model pentru răspunsul unui endpoint
class ExamenResponse(ExamenBase):
    id_Examen: int
    id_Profesor: int

    class Config:
        from_attributes = True
