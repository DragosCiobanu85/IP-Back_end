from database import SessionLocal
from dto.studenti import StudentCreate
from dto.studenti import StudentUpdate
from models import Student

# Funcție pentru a adăuga un student nou
def insert_student(student: StudentCreate):
    db = SessionLocal()
    try:
        db_student = Student(
            nume=student.nume,
            prenume=student.prenume,
            grupa=student.grupa,
            id_Facultate=student.id_Facultate
        )
        db.add(db_student)
        db.commit()
        db.refresh(db_student)
        return db_student
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

# Funcție pentru a obține toți studenții
def get_all_students():
    db = SessionLocal()
    try:
        students = db.query(Student).all()
        return students
    finally:
        db.close()

# Funcție pentru a șterge un student după ID
def delete_student(student_id: int):
    db = SessionLocal()
    try:
        student = db.query(Student).filter(Student.id_Student == student_id).first()
        if student is None:
            return None
        db.delete(student)
        db.commit()
        return student
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

def update_student_rep(student_id: int, student_data: StudentUpdate):
    db = SessionLocal()
    try:
        student = db.query(Student).filter(Student.id_Student == student_id).first()
        if not student:
            return None
        # Actualizează atributele studentului
        student.nume = student_data.nume
        student.prenume = student_data.prenume
        student.grupa = student_data.grupa
        student.id_Facultate = student_data.id_Facultate

        db.commit()
        db.refresh(student)
        return student
    finally:
        db.close()