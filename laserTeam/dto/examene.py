from pydantic import BaseModel, conint
from datetime import time


# Modelul de bază pentru Examen
class ExamenBase(BaseModel):
    ora: time
    sala: str
    id_Profesor: int
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

    class Config:
        from_attributes = True
