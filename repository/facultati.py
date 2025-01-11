from database import SessionLocal
from dto.facultati import FacultateCreate
from repository.studenti import get_student_by_user_id
from models import Grupa, Facultate, Student, User
from auth import get_current_user_id, get_current_user
from fastapi import Depends

def get_facultate_by_student(current_user: User = Depends(get_current_user)):
    db = SessionLocal()
    try:
        # Obține studentul pe baza ID-ului utilizatorului autentificat
        student = db.query(Student).filter(Student.id_user == current_user.id_user).first()
        if not student:
            return None

        # Obține grupa asociată studentului
        grupa = db.query(Grupa).filter(Grupa.id_Grupa == student.id_Grupa).first()
        if not grupa:
            return None

        # Obține facultatea asociată grupei
        facultate = db.query(Facultate).filter(Facultate.id_Facultate == grupa.id_Facultate).first()
        return facultate
    finally:
        db.close()

def insert_facultate(facultate: FacultateCreate):
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
    try:
        return db.query(Facultate).all()
    finally:
        db.close()

def remove_facultate(facultate_id: int):
    db = SessionLocal()
    try:
        facultate = db.query(Facultate).filter(Facultate.id_Facultate == facultate_id).first()
        if facultate is None:
            return None
        db.delete(facultate)
        db.commit()
        return facultate
    finally:
        db.close()
