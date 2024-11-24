from pydantic import BaseModel, validator
from datetime import date

# Modelul de bază pentru Cerere
class CerereBase(BaseModel):
    id_Profesor: int
    id_Facultate: int
    id_Materie: int
    data: date
    status: str

    @validator("status")
    def validate_status(cls, value):
        valid_status = ["in asteptare", "acceptata", "respinsa"]
        if value not in valid_status:
            raise ValueError(f"Status invalid. Trebuie să fie una dintre: {', '.join(valid_status)}")
        return value

# Model pentru crearea unei cereri
class CerereCreate(CerereBase):
    pass

# Model pentru actualizarea unei cereri
class CerereUpdate(BaseModel):
    status: str

# Model pentru răspunsul unui endpoint
class CerereResponse(CerereBase):
    id_Cerere: int

    class Config:
        from_attributes = True
