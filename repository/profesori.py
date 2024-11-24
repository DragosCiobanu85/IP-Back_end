from database import SessionLocal
from dto.profesori import ProfesorCreate, ProfesorUpdate
from models import Profesor

# Funcție pentru a adăuga un profesor nou
def insert_profesor(profesor: ProfesorCreate):
    db = SessionLocal()
    try:
        db_profesor = Profesor(
            nume=profesor.nume,
            prenume=profesor.prenume,
            grad=profesor.grad,
            id_Facultate=profesor.id_Facultate
        )
        db.add(db_profesor)
        db.commit()
        db.refresh(db_profesor)
        return db_profesor
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

# Funcție pentru a obține toți profesorii
def get_all_profesori():
    db = SessionLocal()
    try:
        profesori = db.query(Profesor).all()
        return profesori
    finally:
        db.close()

# Funcție pentru a șterge un profesor după ID
def delete_profesor(profesor_id: int):
    db = SessionLocal()
    try:
        profesor = db.query(Profesor).filter(Profesor.id_Profesor == profesor_id).first()
        if profesor is None:
            return None
        db.delete(profesor)
        db.commit()
        return profesor
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

# Funcție pentru a actualiza un profesor
def update_profesor(profesor_id: int, profesor_data: ProfesorUpdate):
    db = SessionLocal()
    try:
        profesor = db.query(Profesor).filter(Profesor.id_Profesor == profesor_id).first()
        if not profesor:
            return None
        # Actualizează atributele profesorului
        profesor.nume = profesor_data.nume
        profesor.prenume = profesor_data.prenume
        profesor.grad = profesor_data.grad
        profesor.id_Facultate = profesor_data.id_Facultate

        db.commit()
        db.refresh(profesor)
        return profesor
    finally:
        db.close()
