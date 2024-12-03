from database import SessionLocal
from dto.sali import SalaCreate
from models import Sala


def insert_sala(sala: SalaCreate):
    db = SessionLocal()
    try:
        # Validare unicitate
        if db.query(Sala).filter(Sala.nume == sala.nume).first():
            raise ValueError("O facultate cu acest nume există deja.")
        db_sala = Sala(nume=sala.nume)
        db.add(db_sala)
        db.commit()
        db.refresh(db_sala)
        return db_sala
    finally:
        db.close()

def get_all_sali():
    db = SessionLocal()
    sali=db.query(Sala).all()
    db.close()
    return sali

def remove_sala(sala_id: int):
    db = SessionLocal()
    sala = db.query(Sala).filter(Sala.id_Sala == sala_id).first()

    if sala is None:
        db.close()
        return None

    db.delete(sala)
    db.commit()
    db.close()
    return sala

