from pydantic import BaseModel, Field, validator
import re

VALID_TIP_EXAMEN = {"scris", "oral", "moodle", "practic"}

# Modelul de bază pentru Materie
class MaterieBase(BaseModel):
    nume: str
    id_Profesor: int
    tip_examen: str
    an_studiu: int
    semestru: int = Field(..., ge=1, le=8, description="Semestrul trebuie să fie între 1 și 8")

    @validator('nume')
    def validate_nume(cls, value):
        if not re.match(r'^[a-zA-Z0-9 ]+$', value):
            raise ValueError("Numele poate conține doar litere, cifre și spații")
        return value

    @validator('tip_examen')
    def validate_tip_examen(cls, value):
        # Împărțim tipurile pe care le-a introdus utilizatorul
        tipuri = {tip.strip().lower() for tip in value.split(",")}
        if not tipuri.issubset(VALID_TIP_EXAMEN):
            raise ValueError(f"Tipul examenului poate fi doar una dintre valorile: {', '.join(VALID_TIP_EXAMEN)}")
        return value

# Model pentru crearea unei materii
class MaterieCreate(MaterieBase):
    pass

# Model pentru actualizarea unei materii
class MaterieUpdate(MaterieBase):
    pass

# Model pentru răspunsul unui endpoint
class MaterieResponse(MaterieBase):
    id_Materie: int

    class Config:
        from_attributes = True
