from sqlalchemy.orm import Session

from database import SessionLocal
from models import Student
from dto.studenti import StudentCreate


def get_all_students():
    db = SessionLocal()
    return db.query(Student).all()


def get_student_by_id( student_id: int):
    db = SessionLocal()
    return db.query(Student).filter(Student.id_Student == student_id).first()


def insert_student( student: StudentCreate):
    db = SessionLocal()
    db_student = Student(
        nume=student.nume,
        prenume=student.prenume,
        grupa_id=student.grupa_id
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


def delete_student( student_id: int):
    db = SessionLocal()
    try:
        db_student = db.query(Student).filter(Student.id_Student == student_id).first()
        if db_student:
            db.delete(db_student)
            db.commit()
            return True
        return False
    except Exception as e:
        db.rollback()
        raise e
