from pydantic import BaseModel, EmailStr, validator
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    parola: str
    rol: str

    @validator("rol")
    def validate_rol(cls, value):
        if value not in ["Student", "Profesor"]:
            raise ValueError("Rolul trebuie să fie 'Student' sau 'Profesor'")
        return value

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    email: Optional[EmailStr]
    parola: Optional[str]
    rol: Optional[str]

class UserResponse(UserBase):
    id_user: int

    class Config:
        from_attributes= True
