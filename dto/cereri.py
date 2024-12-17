from typing import Optional

from pydantic import BaseModel, validator
from datetime import date

# Modelul de bază pentru Cerere
class CerereBase(BaseModel):
    id_Profesor: int
    id_Facultate: int
    id_Materie: int
    data: date
    status: Optional[str] = None

    # Validare pentru status
    @validator("status", pre=True, always=True)
    def set_status_implicit(cls, v):
        """
        Setăm status-ul implicit dacă nu este furnizat.
        """
        if not v:
            return "in asteptare"  # Status implicit
        if v not in ["in asteptare", "acceptata", "respinsa"]:
            raise ValueError("Statusul trebuie să fie 'in asteptare', 'acceptata' sau 'respinsa'.")
        return v

# Model pentru crearea unei cereri
class CerereCreate(CerereBase):
    pass

# Model pentru actualizarea unei cereri
class CerereUpdate(BaseModel):
    id_Facultate: int
    id_Profesor: int
    id_Materie: int
    data: date
    status: Optional[str] = None

# Model pentru răspunsul unui endpoint
class CerereResponse(CerereBase):
    id_Cerere: int
    id_Student: int
    id_Grupa: int
    status: str

    class Config:
        from_attributes = True
