from pydantic import BaseModel

# DTO pentru crearea unui an de studiu
class AnStudiuCreate(BaseModel):
    an_studiu: int

# DTO pentru actualizarea unui an de studiu
class AnStudiuUpdate(BaseModel):
    an_studiu: int

# DTO pentru răspunsul unui endpoint
class AnStudiuResponse(BaseModel):
    id_An_Studiu: int
    an_studiu: int

    class Config:
        from_attributes = True
