from database import SessionLocal
from models import An_Studiu
from dto.an_studiu import AnStudiuCreate, AnStudiuUpdate

# Funcție pentru a adăuga un nou an de studiu
def create_an_studiu(an_studiu: AnStudiuCreate):
    db = SessionLocal()
    try:
        db_an_studiu = An_Studiu(an_studiu=an_studiu.an_studiu)
        db.add(db_an_studiu)
        db.commit()
        db.refresh(db_an_studiu)
        return db_an_studiu
    finally:
        db.close()

# Funcție pentru a obține toți anii de studiu
def get_all_ani_studiu():
    db = SessionLocal()
    try:
        return db.query(An_Studiu).all()
    finally:
        db.close()

# Funcție pentru a obține un an de studiu după ID
def get_an_studiu_by_id(id_an_studiu: int):
    db = SessionLocal()
    try:
        return db.query(An_Studiu).filter(An_Studiu.id_An_Studiu == id_an_studiu).first()
    finally:
        db.close()

# Funcție pentru a actualiza un an de studiu
def update_an_studiu(id_an_studiu: int, an_studiu: AnStudiuUpdate):
    db = SessionLocal()
    try:
        db_an_studiu = db.query(An_Studiu).filter(An_Studiu.id_An_Studiu == id_an_studiu).first()
        if not db_an_studiu:
            return None
        db_an_studiu.an_studiu = an_studiu.an_studiu
        db.commit()
        db.refresh(db_an_studiu)
        return db_an_studiu
    finally:
        db.close()

# Funcție pentru a șterge un an de studiu
def delete_an_studiu(id_an_studiu: int):
    db = SessionLocal()
    try:
        db_an_studiu = db.query(An_Studiu).filter(An_Studiu.id_An_Studiu == id_an_studiu).first()
        if not db_an_studiu:
            return None
        db.delete(db_an_studiu)
        db.commit()
        return db_an_studiu
    finally:
        db.close()
