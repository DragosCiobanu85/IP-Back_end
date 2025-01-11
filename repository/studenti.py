from database import SessionLocal
from models import Student, Grupa
from dto.studenti import StudentCreate, StudentUpdate

def get_all_students():
    db = SessionLocal()
    try:
        return db.query(Student).all()
    finally:
        db.close()

def get_student_by_user_id(user_id: int):
    db = SessionLocal()
    try:
        return db.query(Student).filter(Student.id_user == user_id).first()
    finally:
        db.close()

def get_student_by_id(student_id: int):
    db = SessionLocal()
    try:
        return db.query(Student).filter(Student.id_Student == student_id).first()
    finally:
        db.close()

def insert_student(student: StudentCreate):
    db = SessionLocal()
    try:
        db_student = Student(
            nume=student.nume,
            prenume=student.prenume,
            id_Grupa=student.id_Grupa,
            id_user=student.id_user,
            id_Specializare=student.id_Specializare
        )
        db.add(db_student)
        db.commit()
        db.refresh(db_student)
        return db_student
    finally:
        db.close()

def get_grupa_by_user(id_user: int):
    db = SessionLocal()
    try:
        student = db.query(Student).filter(Student.id_user == id_user).first()
        if not student:
            return None
        grupa = db.query(Grupa).filter(Grupa.id_Grupa == student.id_Grupa).first()
        return grupa
    finally:
        db.close()

def delete_student(student_id: int):
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
    finally:
        db.close()

def update_student(student_id: int, student_data: StudentUpdate):
    db = SessionLocal()
    try:
        student = db.query(Student).filter(Student.id_Student == student_id).first()
        if not student:
            return None
        if student_data.nume is not None:
            student.nume = student_data.nume
        if student_data.prenume is not None:
            student.prenume = student_data.prenume
        if student_data.grupa_id is not None:
            student.grupa_id = student_data.grupa_id
        if student_data.user_id is not None:
            student.user_id = student_data.user_id
        db.commit()
        db.refresh(student)
        return student
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()
