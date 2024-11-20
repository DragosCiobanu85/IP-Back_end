from sqlalchemy.orm import Session
from database import SessionLocal
from models import Cerere
from dto.cereri import CerereCreate, CerereUpdate

# Funcție pentru a adăuga o cerere nouă
def insert_cerere(cerere: CerereCreate):
    db = SessionLocal()
    try:
        db_cerere = Cerere(
            id_Profesor=cerere.id_Profesor,
            id_Facultate=cerere.id_Facultate,
            id_Materie=cerere.id_Materie,
            data=cerere.data,
            status=cerere.status
        )
        db.add(db_cerere)
        db.commit()
        db.refresh(db_cerere)
        return db_cerere
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

# Funcție pentru a obține toate cererile
def get_all_cereri():
    db = SessionLocal()
    try:
        cereri = db.query(Cerere).all()
        return cereri
    finally:
        db.close()

# Funcție pentru actualizarea statusului unei cereri
def update_cerere(cerere_id: int, cerere_data: CerereUpdate):
    db = SessionLocal()
    try:
        cerere = db.query(Cerere).filter(Cerere.id_Cerere == cerere_id).first()
        if not cerere:
            return None
        cerere.status = cerere_data.status

        db.commit()
        db.refresh(cerere)
        return cerere
    finally:
        db.close()

# Funcție pentru ștergerea unei cereri
def delete_cerere(cerere_id: int):
    db = SessionLocal()
    try:
        cerere = db.query(Cerere).filter(Cerere.id_Cerere == cerere_id).first()
        if not cerere:
            return None
        db.delete(cerere)
        db.commit()
        return cerere
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()
