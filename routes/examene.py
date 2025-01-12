from datetime import timedelta
from fastapi import APIRouter, HTTPException
from typing import List
from models import Examen, User, Cerere, Status
from fastapi import Depends
from auth import get_current_user
from database import SessionLocal
from repository.profesori import get_profesor_by_user_id
from dto.examene import ExamenCreate, ExamenUpdate, ExamenResponse
from repository.examene import insert_examen, get_all_examene, update_examen, delete_examen

from datetime import datetime, timedelta

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

        cerere = db.query(Cerere).filter(Cerere.id_Cerere == examen_data.id_Cerere).first()
        if cerere:
            status = db.query(Status).filter(Status.nume == 'acceptata').first()
            if status:
                cerere.id_Status = status.id_Status
                db.commit()  # Confirmă schimbarea statusului
            else:
                raise HTTPException(status_code=404, detail="Statusul 'acceptata' nu a fost găsit.")

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







@router.get("/examene/sala/{room_id}")
def get_exam_times_for_room(
    room_id: int, 
    requested_date: str  # Data cererii
):
    db = SessionLocal()  # Deschidem o sesiune de bază de date
    try:
        # Convertim requested_date într-un obiect datetime
        requested_date_obj = datetime.strptime(requested_date, "%Y-%m-%d").date()

        # Obținem toate examenele programate pentru sala respectivă
        exams = db.query(Examen).filter(Examen.id_Sala == room_id).all()

        
        # Definim orele disponibile
        all_times = [f"{8 + i}:00:00" for i in range(11)]  # Orele posibile de la 8:00 la 18:00
        available_times = set(all_times)  # Set pentru a facilita eliminarea orelor ocupate
        
        # Extragem orele deja ocupate și le eliminăm din setul de ore disponibile
        for exam in exams:
            start_time = exam.ora
            exam_date = exam.data  # Data examenului
            # Verificăm doar examenele care sunt programate în aceeași dată
            if exam_date == requested_date_obj:
                # Creăm un datetime complet combinând data și ora examenului
                start_datetime = datetime.combine(exam_date, start_time)
                # Adăugăm 2 ore la start_time folosind timedelta
                end_datetime = start_datetime + timedelta(hours=2)

                # Eliminăm ora anterioră și intervalul de 2 ore din setul de ore disponibile
                current_time = start_datetime - timedelta(hours=1)  # Ora x-1 (ora anterioară)
                while current_time < end_datetime:
                    available_times.discard(current_time.strftime("%H:%M:%S"))  # Eliminăm ora ocupată
                    current_time += timedelta(hours=1)

        return list(available_times)
    except Exception as e:
        print(f"Eroare la procesarea cererii: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Eroare la obținerea examenelor: {str(e)}")
    finally:
        db.close()










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