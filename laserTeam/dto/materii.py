from pydantic import BaseModel

# Modelul de bază pentru Materie
class MaterieBase(BaseModel):
    nume: str
    id_Profesor: int
    tip_examen: str
    an_studiu: int
    semestru: int

# Model pentru crearea unei materii
class MaterieCreate(MaterieBase):
    pass

# Model pentru actualizarea unei materii
class MaterieUpdate(MaterieBase):
    pass

# Model pentru răspunsul unui endpoint
class MaterieResponse(MaterieBase):
    id_Materie: int

    class Config:
        from_attributes = True
