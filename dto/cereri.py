from pydantic import BaseModel, validator
from datetime import date

# Modelul de bază pentru Cerere
class CerereBase(BaseModel):
    id_Profesor: int
    id_Facultate: int
    id_Materie: int
    data: date
    
# Model pentru crearea unei cereri
class CerereCreate(CerereBase):
    pass

# Model pentru actualizarea unei cereri
class CerereUpdate(BaseModel):
    id_Facultate: int
    id_Profesor: int
    id_Materie: int
    data: date

# Model pentru răspunsul unui endpoint
class CerereResponse(CerereBase):
    id_Cerere: int
    id_Student: int
    id_Grupa: int

    class Config:
        from_attributes = True
