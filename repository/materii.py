from sqlalchemy.orm import Session
from database import SessionLocal
from models import Materie
from dto.materii import MaterieCreate, MaterieUpdate

# Funcție pentru a adăuga o materie nouă
def insert_materie(materie: MaterieCreate):
    db = SessionLocal()
    try:
        db_materie = Materie(
            nume=materie.nume,
            id_Profesor=materie.id_Profesor,
            tip_examen=materie.tip_examen,
            an_studiu=materie.an_studiu,
            semestru=materie.semestru
        )
        db.add(db_materie)
        db.commit()
        db.refresh(db_materie)
        return db_materie
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

# Funcție pentru a obține toate materiile
def get_all_materii():
    db = SessionLocal()
    try:
        materii = db.query(Materie).all()
        return materii
    finally:
        db.close()

# Funcție pentru actualizarea unei materii
def update_materie(materie_id: int, materie_data: MaterieUpdate):
    db = SessionLocal()
    try:
        materie = db.query(Materie).filter(Materie.id_Materie == materie_id).first()
        if not materie:
            return None
        materie.nume = materie_data.nume
        materie.id_Profesor = materie_data.id_Profesor
        materie.tip_examen = materie_data.tip_examen
        materie.an_studiu = materie_data.an_studiu
        materie.semestru = materie_data.semestru

        db.commit()
        db.refresh(materie)
        return materie
    finally:
        db.close()

# Funcție pentru ștergerea unei materii
def delete_materie(materie_id: int):
    db = SessionLocal()
    try:
        materie = db.query(Materie).filter(Materie.id_Materie == materie_id).first()
        if not materie:
            return None
        db.delete(materie)
        db.commit()
        return materie
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()
