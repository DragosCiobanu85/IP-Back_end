from sqlalchemy.orm import Session
from database import SessionLocal
from models import Examen, User
from fastapi import Depends
from repository.profesori import get_profesor_by_user_id
from dto.examene import ExamenCreate, ExamenUpdate
from auth import get_current_user


# Funcție pentru a adăuga un examen nou
def insert_examen(examen: ExamenCreate, current_user: User = Depends(get_current_user)):
    db = SessionLocal()
    try:

        profesor = get_profesor_by_user_id(current_user.id_user)
        db_examen = Examen(
            id_Facultate=examen.id_Facultate,
            id_Grupa=examen.id_Grupa,
            id_Profesor_1=examen.id_Profesor_1,
            id_Profesor=profesor.id_Profesor,
            id_Materie=examen.id_Materie,
            data=examen.data,
            id_Sala=examen.id_Sala,
            ora=examen.ora,
            id_Cerere=examen.id_Cerere
        )
        db.add(db_examen)
        db.commit()
        db.refresh(db_examen)
        return db_examen
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


# Funcție pentru a obține toate examenele
def get_all_examene():
    db = SessionLocal()
    try:
        examene = db.query(Examen).all()
        return examene
    finally:
        db.close()


# Funcție pentru actualizarea unui examen
def update_examen(examen_id: int, examen_data: ExamenUpdate):
    db = SessionLocal()
    try:
        examen = db.query(Examen).filter(Examen.id_Examen == examen_id).first()
        if not examen:
            return None
        examen.ora = examen_data.ora
        examen.sala = examen_data.sala

        db.commit()
        db.refresh(examen)
        return examen
    finally:
        db.close()


# Funcție pentru ștergerea unui examen
def delete_examen(examen_id: int):
    db = SessionLocal()
    try:
        examen = db.query(Examen).filter(Examen.id_Examen == examen_id).first()
        if not examen:
            return None
        db.delete(examen)
        db.commit()
        return examen
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()
