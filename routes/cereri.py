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
        if current_user.rol != "Student":
            raise HTTPException(status_code=403, detail="Doar studenții pot crea cereri.")

        student = get_student_by_user_id(current_user.id_user)

        if not student:
            raise HTTPException(status_code=404, detail="Studentul nu a fost găsit.")

        new_cerere = Cerere(
            id_Profesor=cerere_data.id_Profesor,
            id_Facultate=cerere_data.id_Facultate,
            id_Materie=cerere_data.id_Materie,
            id_Student=student.id_Student,
            id_Grupa=student.id_Grupa,
            data=cerere_data.data,
            status=cerere_data.status  # Setăm status-ul
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

    student = get_student_by_user_id(current_user.id_user)
    updated_cerere = update_cerere(cerere_id, cerere, student.id_user)

    if not updated_cerere:
        raise HTTPException(status_code=404, detail="Cerere not found")
    
    return updated_cerere


@router.put("/cereri/{cerere_id}/status", response_model=CerereResponse)
def update_status(cerere_id: int, status: str, current_user: User = Depends(get_current_user)):
    """
    Endpoint pentru actualizarea statusului unei cereri.
    Numai profesorii pot schimba statusul.
    """
    db = SessionLocal()
    try:
        # Verificăm dacă utilizatorul este profesor
        if current_user.rol != "Profesor":
            raise HTTPException(status_code=403, detail="Doar profesorii pot actualiza statusul cererilor.")

        cerere = db.query(Cerere).filter(Cerere.id_Cerere == cerere_id).first()
        if not cerere:
            raise HTTPException(status_code=404, detail="Cererea nu a fost găsită.")

        # Validare status
        if status not in ["acceptata", "respinsa"]:
            raise HTTPException(status_code=400, detail="Statusul trebuie să fie 'acceptata' sau 'respinsa'.")

        # Actualizăm statusul
        cerere.status = status
        db.commit()
        db.refresh(cerere)
        return cerere

    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


# Endpoint pentru ștergerea unei cereri
@router.delete("/cereri/{cerere_id}", response_model=CerereResponse)
def delete_cerere_endpoint(cerere_id: int):
    print(f"Ștergere cerere cu id: {cerere_id}")
    deleted_cerere = delete_cerere(cerere_id)
    if not deleted_cerere:
        raise HTTPException(status_code=404, detail="Cerere not found")
    return deleted_cerere
