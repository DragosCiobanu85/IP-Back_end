from fastapi import APIRouter, HTTPException
from typing import List
from models import Examen, User
from fastapi import Depends
from auth import get_current_user
from database import SessionLocal
from repository.profesori import get_profesor_by_user_id
from dto.examene import ExamenCreate, ExamenUpdate, ExamenResponse
from repository.examene import insert_examen, get_all_examene, update_examen, delete_examen

router = APIRouter()
# Endpoint pentru a adăuga un examen
@router.post("/examene/", response_model=ExamenResponse)
def create_examen(
    examen_data: ExamenCreate, 
    current_user: User = Depends(get_current_user)
):
    db = SessionLocal()
    try:
        # Logăm informațiile despre utilizatorul curent
        print(f"current_user: {current_user.rol}")

        # Verificăm dacă utilizatorul curent este profesor
        if current_user.rol != "Profesor":
            raise HTTPException(status_code=403, detail="Doar profesorii pot crea examene.")

        # Obținem profesorul pe baza user_id
        profesor = get_profesor_by_user_id(current_user.id_user)
        
        # Verificăm dacă am găsit profesorul
        if profesor:
            print(f"Profesor găsit: {profesor.id_Profesor}")
        else:
            print(f"Profesorul cu id_user {current_user.id_user} nu a fost găsit.")
        
        if not profesor:
            raise HTTPException(status_code=404, detail="Profesorul nu a fost găsit.")

        # Creăm examenul folosind datele din cererea HTTP
        new_examen = Examen(
            id_Facultate=examen_data.id_Facultate,
            id_Grupa=examen_data.id_Grupa,
            id_Profesor_1=examen_data.id_Profesor_1,
            id_Profesor=profesor.id_Profesor,
            id_Materie=examen_data.id_Materie,
            data=examen_data.data,
            id_Sala=examen_data.id_Sala,
            ora=examen_data.ora,
            id_Cerere=examen_data.id_Cerere
        )

        print(f"Creare examen cu id_Profesor: {profesor.id_Profesor}, id_Materie: {examen_data.id_Materie}")

        # Adăugăm examenul în baza de date
        db.add(new_examen)
        db.commit()
        db.refresh(new_examen)
        print(f"Examen creat cu id: {new_examen.id_Examen}")
        
        # Returnăm examenul creat
        return new_examen

    except Exception as e:
        print(f"Eroare la crearea examenului: {str(e)}")
        db.rollback()
        raise e
    finally:
        db.close()



# Endpoint pentru a obține toate examenele
@router.get("/examene/", response_model=List[ExamenResponse])
def read_examene():
    return get_all_examene()


# Endpoint pentru actualizarea unui examen
@router.put("/examene/{examen_id}", response_model=ExamenResponse)
def update_examen_endpoint(examen_id: int, examen: ExamenUpdate):
    updated_examen = update_examen(examen_id, examen)
    if not updated_examen:
        raise HTTPException(status_code=404, detail="Examen not found")
    return updated_examen


# Endpoint pentru ștergerea unui examen
@router.delete("/examene/{examen_id}", response_model=ExamenResponse)
def delete_examen_endpoint(examen_id: int):
    deleted_examen = delete_examen(examen_id)
    if not deleted_examen:
        raise HTTPException(status_code=404, detail="Examen not found")
    return deleted_examen