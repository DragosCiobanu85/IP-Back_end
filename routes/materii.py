from fastapi import APIRouter, HTTPException
from typing import List
from dto.materii import MaterieCreate, MaterieUpdate, MaterieResponse
from dto.profesori import ProfesorResponse
from repository.materii import insert_materie, get_all_materii, update_materie, delete_materie, get_profesor_by_materie
from models import User, Materie, Student, Grupa
from fastapi import Depends
from database import SessionLocal
from auth import get_current_user
from datetime import datetime
router = APIRouter()
# Endpoint pentru a adăuga o materie
@router.post("/materii/", response_model=MaterieResponse)
def create_materie(materie: MaterieCreate):
    db_materie = insert_materie(materie)
    return db_materie

# Endpoint pentru a obține toate materiile
@router.get("/materii/", response_model=List[MaterieResponse])
def read_materii():
    return get_all_materii()

@router.get("/materii/{id_materie}/profesor", response_model=ProfesorResponse)
def get_profesor_endpoint(id_materie: int):
    profesor = get_profesor_by_materie(id_materie)
    if not profesor:
        raise HTTPException(status_code=404, detail="Profesorul asociat materiei nu a fost găsit.")
    return profesor



@router.get("/materii/filter", response_model=List[MaterieResponse])
def get_filtered_materii(current_user: User = Depends(get_current_user)):
    db = SessionLocal()
    try:
        # Obține grupa studentului
        student = db.query(Student).filter(Student.id_user == current_user.id_user).first()
        if not student:
            raise HTTPException(status_code=404, detail="Studentul nu a fost găsit.")

        grupa = db.query(Grupa).filter(Grupa.id_Grupa == student.id_Grupa).first()
        if not grupa:
            raise HTTPException(status_code=404, detail="Grupa nu a fost găsită.")

        id_an_studiu = grupa.id_An_Studiu

        # Determină semestrul curent în funcție de luna curentă
        current_month = datetime.now().month
        semestru_curent = 1 if current_month >= 10 or current_month <= 3 else 2

        # Filtrează materiile pe baza anului de studiu și semestrului curent
        materii = db.query(Materie).filter(
            Materie.id_Specializare == student.id_Specializare,
            Materie.id_An_Studiu == id_an_studiu,
            Materie.semestru == semestru_curent
        ).all()

        if not materii:
            raise HTTPException(status_code=404, detail="Nu s-au găsit materii pentru semestrul curent.")

        return materii
    finally:
        db.close()




# Endpoint pentru actualizarea unei materii
@router.put("/materii/{materie_id}", response_model=MaterieResponse)
def update_materie_endpoint(materie_id: int, materie: MaterieUpdate):
    updated_materie = update_materie(materie_id, materie)
    if not updated_materie:
        raise HTTPException(status_code=404, detail="Materie not found")
    return updated_materie

# Endpoint pentru ștergerea unei materii
@router.delete("/materii/{materie_id}", response_model=MaterieResponse)
def delete_materie_endpoint(materie_id: int):
    deleted_materie = delete_materie(materie_id)
    if not deleted_materie:
        raise HTTPException(status_code=404, detail="Materie not found")
    return deleted_materie
