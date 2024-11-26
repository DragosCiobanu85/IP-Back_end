from sqlalchemy.orm import Session

from database import SessionLocal
from models import Grupa
from dto.grupe import GrupaCreate, GrupaUpdate

def grupa_exists(nume: str):
    db = SessionLocal()
    exists = db.query(Grupa).filter(Grupa.nume == nume).first()
    db.close()
    return exists is not None
# Funcție pentru a adăuga o grupă nouă
def insert_grupa( grupa: GrupaCreate):
    if grupa_exists(grupa.nume):
        raise ValueError("Grupa cu acest nume există deja.")
    db_grupa = Grupa(nume=grupa.nume, facultate_id=grupa.facultate_id)
    db = SessionLocal()
    db.add(db_grupa)
    db.commit()
    db.refresh(db_grupa)
    return db_grupa

# Funcție pentru a obține o grupă după ID
def get_grupa_by_id( grupa_id: int):
    db = SessionLocal()
    return db.query(Grupa).filter(Grupa.id_Grupa == grupa_id).first()

# Funcție pentru a obține toate grupele
def get_all_grupe():
    db = SessionLocal()
    return db.query(Grupa).all()

# Funcție pentru a șterge o grupă după ID
def delete_grupa( grupa_id: int):
    db = SessionLocal()
    grupa = db.query(Grupa).filter(Grupa.id_Grupa == grupa_id).first()
    if grupa:
        db.delete(grupa)
        db.commit()
    return grupa

# Funcție pentru a actualiza o grupă
def update_grupa(grupa_id: int, grupa_data: GrupaUpdate):
    db = SessionLocal()
    grupa = db.query(Grupa).filter(Grupa.id_Grupa == grupa_id).first()
    if not grupa:
        return None
    if grupa_data.nume:
        grupa.nume = grupa_data.nume
    if grupa_data.facultate_id:
        grupa.facultate_id = grupa_data.facultate_id
    db.commit()
    db.refresh(grupa)
    return grupa
