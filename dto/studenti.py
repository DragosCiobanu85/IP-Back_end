from pydantic import BaseModel, StringConstraints
from typing import Annotated, Optional


class StudentBase(BaseModel):
    nume: Annotated[str, StringConstraints(pattern=r"^[a-zA-Z\s-]+$", min_length=2, max_length=50)]
    prenume: Annotated[str, StringConstraints(pattern=r"^[a-zA-Z\s-]+$", min_length=2, max_length=50)]
    id_Grupa: int
    id_user: int

    class Config:
        from_attributes = True


class StudentCreate(StudentBase):
    pass


class StudentResponse(StudentBase):
    id_Student: int


    class Config:
        from_attributes = True
    


class StudentUpdate(BaseModel):
  
    nume: Optional[Annotated[str, StringConstraints(pattern=r"^[a-zA-Z\s-]+$", min_length=2, max_length=50)]]
    prenume: Optional[Annotated[str, StringConstraints(pattern=r"^[a-zA-Z\s-]+$", min_length=2, max_length=50)]]
    id_Grupa: Optional[int]
    id_user: Optional[int]

    class Config:

        from_attributes = True

