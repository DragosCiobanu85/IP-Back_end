# Modelul Pydantic pentru datele Facultate
from pydantic import BaseModel,validator,StringConstraints
from typing import Annotated

class FacultateBase(BaseModel):
    nume: Annotated[
        str,
        StringConstraints(pattern=r"^[a-zA-Z\s]+$", min_length=2, max_length=100)
    ]

    @validator('nume')
    def normalize_name(cls, value):
        restricted_names = ["N/A", "---", "Test"]
        value = value.strip()
        if value in restricted_names:
            raise ValueError(f"Numele '{value}' nu este permis.")
        return value

class FacultateCreate(FacultateBase):
    pass

class FacultateResponse(FacultateBase):
    id_Facultate: int

    class Config:
        from_attributes = True