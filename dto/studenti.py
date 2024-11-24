from pydantic import BaseModel

class StudentBase(BaseModel):
    nume: str
    prenume: str
    grupa_id: int

    class Config:
        from_attributes = True


class StudentCreate(StudentBase):
    pass


class StudentResponse(StudentBase):
    id_Student: int

    class Config:
        from_attributes = True
