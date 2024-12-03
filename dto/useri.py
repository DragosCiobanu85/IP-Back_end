from pydantic import BaseModel, EmailStr, validator
from typing import Optional
import re

class UserBase(BaseModel):
    email: EmailStr
    parola: str
    rol: str

    @validator("rol")
    def validate_rol(cls, value):
        if value not in ["Student", "Profesor"]:
            raise ValueError("Rolul trebuie să fie 'Student' sau 'Profesor'")
        return value

    @validator("parola")
    def validate_parola(cls, value):
        if len(value) < 8:
            raise ValueError("Parola trebuie să aibă cel puțin 8 caractere.")
        if not re.search(r"[A-Za-z]", value):
            raise ValueError("Parola trebuie să conțină cel puțin o literă.")
        if not re.search(r"\d", value):
            raise ValueError("Parola trebuie să conțină cel puțin o cifră.")
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

class UserLogin(BaseModel):
    email: EmailStr
    password: str