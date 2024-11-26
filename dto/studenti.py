from pydantic import BaseModel,StringConstraints
from typing import Annotated, Optional


class StudentBase(BaseModel):
    nume: Annotated[str, StringConstraints(pattern=r"^[a-zA-Z\s-]+$", min_length=2, max_length=50)]
    prenume: Annotated[str, StringConstraints(pattern=r"^[a-zA-Z\s-]+$", min_length=2, max_length=50)]
    grupa_id: int

    class Config:
        from_attributes = True


class StudentCreate(StudentBase):
    pass


class StudentResponse(StudentBase):
    id_Student: int

    class Config:
        from_attributes = True

class StudentUpdate(BaseModel):
    # Câmpurile sunt opționale pentru actualizare
    nume: Optional[Annotated[str, StringConstraints(pattern=r"^[a-zA-Z\s-]+$", min_length=2, max_length=50)]]
    prenume: Optional[Annotated[str, StringConstraints(pattern=r"^[a-zA-Z\s-]+$", min_length=2, max_length=50)]]
    grupa_id: Optional[int]