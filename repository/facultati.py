from database import SessionLocal
from dto.facultati import FacultateCreate
from models import Facultate


def insert_faculate(facultate: FacultateCreate):
    db = SessionLocal()
    try:
        # Validare unicitate
        if db.query(Facultate).filter(Facultate.nume == facultate.nume).first():
            raise ValueError("O facultate cu acest nume există deja.")
        db_facultate = Facultate(nume=facultate.nume)
        db.add(db_facultate)
        db.commit()
        db.refresh(db_facultate)
        return db_facultate
    finally:
        db.close()

def get_all_facultati():
    db = SessionLocal()
    facultati=db.query(Facultate).all()
    db.close()
    return facultati

def remove_facultate(facultate_id: int):
    db = SessionLocal()
    facultate = db.query(Facultate).filter(Facultate.id_Facultate == facultate_id).first()

    if facultate is None:
        db.close()
        return None

    db.delete(facultate)
    db.commit()
    db.close()
    return facultate

