# Modelul Pydantic pentru datele Profesor
from pydantic import BaseModel,validator
import re
from typing import Optional

class ProfesorBase(BaseModel):
    nume: str
    prenume: str
    grad: str
    id_Facultate: int
    id_user: int

    @validator("nume")
    def validate_nume(cls, value):
        if not re.match(r"^[a-zA-Z\-]+$", value):
            raise ValueError("Numele trebuie să conțină doar litere și cratime.")
        return value

    @validator("prenume")
    def validate_prenume(cls, value):
        if not re.match(r"^[a-zA-Z\-]+$", value):
            raise ValueError("Prenumele trebuie să conțină doar litere și cratime.")
        return value

    @validator("grad")
    def validate_grad(cls, value):
        valid_grades = ["Asistent", "Lector", "Conferentiar", "Profesor"]
        if value not in valid_grades:
            raise ValueError(f"Gradul trebuie să fie unul dintre: {', '.join(valid_grades)}")
        return value


class ProfesorCreate(ProfesorBase):
    pass

class ProfesorUpdate(BaseModel):
    nume: Optional[str]
    prenume: Optional[str]
    grad: Optional[str]
    id_Facultate: Optional[int]
    id_user: Optional[int]

    @validator("nume")
    def validate_nume(cls, value):
        if value and not re.match(r"^[a-zA-Z\-]+$", value):
            raise ValueError("Numele trebuie să conțină doar litere și cratime.")
        return value

    @validator("prenume")
    def validate_prenume(cls, value):
        if value and not re.match(r"^[a-zA-Z\-]+$", value):
            raise ValueError("Prenumele trebuie să conțină doar litere și cratime.")
        return value

    @validator("grad")
    def validate_grad(cls, value):
        valid_grades = ["Asistent", "Lector", "Conferentiar", "Profesor"]
        if value and value not in valid_grades:
            raise ValueError(f"Gradul trebuie să fie unul dintre: {', '.join(valid_grades)}")
        return value

class ProfesorResponse(ProfesorBase):
    id_Profesor: int

    class Config:
        from_attributes = True

