# repository/status.py

from models import Status
from database import SessionLocal
from dto.status import StatusCreate, StatusUpdate

def get_all_statusuri():
    db = SessionLocal()  # Inițializarea sesiunii DB
    try:
        return db.query(Status).all()
    finally:
        db.close()

def get_status_by_id(id_status: int):
    db = SessionLocal()
    try:
        return db.query(Status).filter(Status.id_Status == id_status).first()
    finally:
        db.close()

def create_status(status: StatusCreate):
    db = SessionLocal()
    try:
        db_status = Status(nume=status.nume)
        db.add(db_status)
        db.commit()
        db.refresh(db_status)
        return db_status
    finally:
        db.close()

def update_status(id_status: int, status: StatusUpdate):
    db = SessionLocal()
    try:
        db_status = db.query(Status).filter(Status.id_Status == id_status).first()
        if db_status:
            db_status.nume = status.nume
            db.commit()
            db.refresh(db_status)
            return db_status
        return None
    finally:
        db.close()

def delete_status(id_status: int):
    db = SessionLocal()
    try:
        db_status = db.query(Status).filter(Status.id_Status == id_status).first()
        if db_status:
            db.delete(db_status)
            db.commit()
            return db_status
        return None
    finally:
        db.close()
