from fastapi import APIRouter, HTTPException
from typing import List
from database import SessionLocal
from dto.cereri import CerereCreate, CerereUpdate, CerereResponse
from repository.cereri import insert_cerere, get_all_cereri, update_cerere, delete_cerere
from auth import get_current_user_id, get_current_user
from repository.studenti import get_student_by_user_id
from fastapi import Depends
from models import Cerere, User

router = APIRouter()

# Endpoint pentru a adăuga o cerere
@router.post("/cereri/", response_model=CerereResponse)
def create_cerere(
    cerere_data: CerereCreate,
    current_user: User = Depends(get_current_user)
):
    db = SessionLocal()
    try:
        print(f"current_user: {current_user.rol}")
        # Verificăm dacă utilizatorul curent este student
        

        if current_user.rol != "Student":
            raise HTTPException(status_code=403, detail="Doar studenții pot crea cereri.")

        # Găsim studentul pe baza id_user al utilizatorului curent
        student = get_student_by_user_id(current_user.id_user)
        
        # Verificăm dacă am găsit studentul
        if student:
            print(f"Student găsit: {student.id_Student}")
        else:
            print(f"Studentul cu id_user {current_user.id_user} nu a fost găsit.")
        
        if not student:
            raise HTTPException(status_code=404, detail="Studentul nu a fost găsit.")

        # Creăm cererea și completăm automat id_Student
        new_cerere = Cerere(
            id_Profesor=cerere_data.id_Profesor,
            id_Facultate=cerere_data.id_Facultate,
            id_Materie=cerere_data.id_Materie,
            id_Student=student.id_Student, 
            id_Grupa=student.id_Grupa, # Autocompletăm id_grupa
            data=cerere_data.data
        )

        print(f"Creare cerere cu id_Student: {student.id_Student}, id_Profesor: {cerere_data.id_Profesor}")

        db.add(new_cerere)
        db.commit()
        db.refresh(new_cerere)
        print(f"Cerere creată cu id: {new_cerere.id_Cerere}")
        return new_cerere

    except Exception as e:
        print(f"Eroare la crearea cererii: {str(e)}")
        db.rollback()
        raise e
    finally:
        db.close()

# Endpoint pentru a obține toate cererile
@router.get("/cereri/", response_model=List[CerereResponse])
def read_cereri(current_user_id: int = Depends(get_current_user_id)):
    """
    Obține cererile de examen. Dacă utilizatorul este profesor, va vedea doar cererile
    asociate cu el. Dacă este admin, poate vedea toate cererile.
    """
    print(f"Citirea cererilor pentru user_id: {current_user_id}")
    return get_all_cereri(current_user_id)


# Endpoint pentru actualizarea statusului unei cereri
@router.put("/cereri/{cerere_id}", response_model=CerereResponse)
def update_cerere_endpoint(cerere_id: int, cerere: CerereUpdate, current_user: User = Depends(get_current_user)):
    """
    Endpoint for updating a request (cerere) by its ID.
    The `user_id` will be automatically extracted from the JWT token.
    """
    print(f"Actualizare cerere cu id: {cerere_id}")
    # Now, we pass `user_id` instead of `token`
    student = get_student_by_user_id(current_user.id_user)
    updated_cerere = update_cerere(cerere_id, cerere, student.id_user)
    
    if not updated_cerere:
        raise HTTPException(status_code=404, detail="Cerere not found")
    
    return updated_cerere

# Endpoint pentru ștergerea unei cereri
@router.delete("/cereri/{cerere_id}", response_model=CerereResponse)
def delete_cerere_endpoint(cerere_id: int):
    print(f"Ștergere cerere cu id: {cerere_id}")
    deleted_cerere = delete_cerere(cerere_id)
    if not deleted_cerere:
        raise HTTPException(status_code=404, detail="Cerere not found")
    return deleted_cerere
