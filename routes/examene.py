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
            id_Specializare=examen_data.id_Specializare,
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
    requested_date: str,
):
    db = SessionLocal()  # Deschidem o sesiune de bază de date
    try:
        # Convertim requested_date într-un obiect datetime
        requested_date_obj = datetime.strptime(requested_date, "%Y-%m-%d").date()

        # Obținem toate examenele programate pentru sala respectivă
        exams = (
            db.query(Examen)
            .filter(Examen.id_Sala == room_id, Examen.data == requested_date_obj)
            .order_by(Examen.ora)
            .all()
        )

        # Construim toate orele posibile de la 8:00 la 18:00
        all_times = [
            datetime.combine(requested_date_obj, datetime.strptime(f"{8 + i}:00:00", "%H:%M:%S").time())
            for i in range(11)
        ]

        # Ore indisponibile
        unavailable_times = set()

        # Marcam orele ocupate și intervalele de 2 ore
        for exam in exams:
            start_datetime = datetime.combine(requested_date_obj, exam.ora)
            end_datetime = start_datetime + timedelta(hours=2)

            # Excludem orele din intervalul [ora - 1, ora + 2)
            current_time = start_datetime - timedelta(hours=1)
            while current_time < end_datetime:
                unavailable_times.add(current_time)
                current_time += timedelta(hours=1)

        # Validăm orele disponibile
        available_times = []
        for time in all_times:
            if time in unavailable_times:
                continue

            # Verificăm dacă există cel puțin 2 ore libere înainte sau după
            prev_time_1 = time - timedelta(hours=1)
            prev_time_2 = time - timedelta(hours=2)
            next_time_1 = time + timedelta(hours=1)
            next_time_2 = time + timedelta(hours=2)

            if (
                (prev_time_1 not in unavailable_times or prev_time_2 not in unavailable_times)
                or (next_time_1 not in unavailable_times or next_time_2 not in unavailable_times)
            ):
                available_times.append(time.strftime("%H:%M:%S"))

        return available_times

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