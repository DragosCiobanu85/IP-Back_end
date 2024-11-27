from sqlalchemy.orm import Session

from database import SessionLocal
from models import Student
from dto.studenti import StudentCreate, StudentUpdate


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
        grupa_id=student.grupa_id,
        id_user=student.id_user
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


def update_student(student_id: int, student_data: StudentUpdate):
    db = SessionLocal()
    try:
        # Găsim studentul în baza de date
        student = db.query(Student).filter(Student.id_Student == student_id).first()
        if not student:
            return None

        # Actualizăm câmpurile primite
        if student_data.nume is not None:
            student.nume = student_data.nume
        if student_data.prenume is not None:
            student.prenume = student_data.prenume
        if student_data.grupa_id is not None:
            student.grupa_id = student_data.grupa_id
        if student_data.user_id is not None:
            student.user_id = student_data.user_id
        # Salvăm modificările
        db.commit()
        db.refresh(student)
        return student
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()