from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    parola: str
    rol: str

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    email: Optional[EmailStr]
    parola: Optional[str]
    rol: Optional[str]

class UserResponse(UserBase):
    id_user: int

    class Config:
        orm_mode = True
