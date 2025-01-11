from database import SessionLocal
from models import Specializare, Student
from dto.specializare import SpecializareCreate, SpecializareUpdate

# Funcție pentru a adăuga o nouă specializare
def create_specializare(specializare: SpecializareCreate):
    db = SessionLocal()
    try:
        db_specializare = Specializare(
            nume=specializare.nume,
            id_Facultate=specializare.id_Facultate
        )
        db.add(db_specializare)
        db.commit()
        db.refresh(db_specializare)
        return db_specializare
    finally:
        db.close()

# Funcție pentru a obține specializarea studentului pentru o facultate
def get_specializare_by_user_and_facultate(id_user: int, id_facultate: int):
    db = SessionLocal()
    try:
        student = db.query(Student).filter(Student.id_user == id_user).first()
        if not student:
            return None
        specializare = (
            db.query(Specializare)
            .filter(Specializare.id_Specializare == student.id_Specializare)
            .filter(Specializare.id_Facultate == id_facultate)
            .first()
        )
        return specializare
    finally:
        db.close()

# Funcție pentru a obține toate specializările
def get_all_specializari():
    db = SessionLocal()
    try:
        return db.query(Specializare).all()
    finally:
        db.close()

# Funcție pentru a obține o specializare după ID
def get_specializare_by_id(id_specializare: int):
    db = SessionLocal()
    try:
        return db.query(Specializare).filter(Specializare.id_Specializare == id_specializare).first()
    finally:
        db.close()

# Funcție pentru a actualiza o specializare
def update_specializare(id_specializare: int, specializare: SpecializareUpdate):
    db = SessionLocal()
    try:
        db_specializare = db.query(Specializare).filter(Specializare.id_Specializare == id_specializare).first()
        if not db_specializare:
            return None
        if specializare.nume is not None:
            db_specializare.nume = specializare.nume
        if specializare.id_Facultate is not None:
            db_specializare.id_Facultate = specializare.id_Facultate
        db.commit()
        db.refresh(db_specializare)
        return db_specializare
    finally:
        db.close()

# Funcție pentru a șterge o specializare
def delete_specializare(id_specializare: int):
    db = SessionLocal()
    try:
        db_specializare = db.query(Specializare).filter(Specializare.id_Specializare == id_specializare).first()
        if not db_specializare:
            return None
        db.delete(db_specializare)
        db.commit()
        return db_specializare
    finally:
        db.close()
