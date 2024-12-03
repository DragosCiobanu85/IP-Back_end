# Modelul Pydantic pentru datele Facultate
from pydantic import BaseModel,validator,StringConstraints
from typing import Annotated

class SalaBase(BaseModel):
    nume: Annotated[
        str,
        StringConstraints(pattern=r"^[a-zA-Z0-9\s]+$", min_length=2, max_length=50)
    ]

    @validator('nume')
    def normalize_name(cls, value):
        restricted_names = ["N/A", "---", "Test"]
        value = value.strip()
        if value in restricted_names:
            raise ValueError(f"Numele '{value}' nu este permis.")
        return value

class SalaCreate(SalaBase):
    pass

class SalaResponse(SalaBase):
    id_Sala: int

    class Config:
        from_attributes = True