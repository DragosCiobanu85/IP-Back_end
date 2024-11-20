from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import SessionLocal, engine
import models
from dto.facultati import FacultateResponse, FacultateCreate
from repository.facultati import insert_faculate, get_all_facultati, remove_facultate

from dto.studenti import StudentResponse, StudentCreate, StudentUpdate
from repository.studenti import insert_student, get_all_students, delete_student,update_student_rep

from dto.profesori import ProfesorResponse, ProfesorCreate, ProfesorUpdate
from repository.profesori import insert_profesor, get_all_profesori, delete_profesor, update_profesor

# Crează tabelele în baza de date (dacă nu există deja)
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Endpoint pentru a adăuga o facultate
@app.post("/facultati/", response_model=FacultateResponse)
def create_facultate(facultate: FacultateCreate):
    db_facultate = insert_faculate(facultate)
    return db_facultate


# Endpoint pentru a lista toate facultățile
@app.get("/facultati/", response_model=List[FacultateResponse])
def read_facultati():
    return get_all_facultati()



@app.delete("/facultati/{facultate_id}", response_model=FacultateResponse)
def delete_facultate(facultate_id: int):
    deleted_facultate = remove_facultate(facultate_id)  # Apelează funcția modificată
    if deleted_facultate is None:
        raise HTTPException(status_code=404, detail="Facultatea nu a fost găsită")
    return deleted_facultate

#-------Studenti--------

# Endpoint pentru a adăuga un student nou
@app.post("/students/", response_model=StudentResponse)
def create_student(student: StudentCreate):
    try:
        db_student = insert_student(student)
        return db_student
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint pentru a prelua toți studenții
@app.get("/students/", response_model=List[StudentResponse])
def read_students():
    try:
        return get_all_students()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint pentru a șterge un student după ID
@app.delete("/students/{student_id}", response_model=StudentResponse)
def remove_student(student_id: int):
    try:
        deleted_student = delete_student(student_id)
        if deleted_student is None:
            raise HTTPException(status_code=404, detail="Studentul nu a fost găsit")
        return deleted_student
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint pentru actualizarea unui student
@app.put("/students/{student_id}", response_model=StudentResponse)
def update_student(student_id: int, student: StudentUpdate):
    updated_student = update_student_rep(student_id, student)
    if not updated_student:
        raise HTTPException(status_code=404, detail="Student not found")
    return updated_student


#----------Profesori---------------

# Endpoint pentru a adăuga un profesor
@app.post("/profesori/", response_model=ProfesorResponse)
def create_profesor(profesor: ProfesorCreate):
    db_profesor = insert_profesor(profesor)
    return db_profesor

# Endpoint pentru a obține toți profesorii
@app.get("/profesori/", response_model=List[ProfesorResponse])
def read_profesori():
    return get_all_profesori()

# Endpoint pentru a șterge un profesor după ID
@app.delete("/profesori/{profesor_id}", response_model=ProfesorResponse)
def delete_profesor_endpoint(profesor_id: int):
    profesor = delete_profesor(profesor_id)
    if not profesor:
        raise HTTPException(status_code=404, detail="Profesor not found")
    return profesor

# Endpoint pentru a actualiza un profesor
@app.put("/profesori/{profesor_id}", response_model=ProfesorResponse)
def update_profesor_endpoint(profesor_id: int, profesor: ProfesorUpdate):
    updated_profesor = update_profesor(profesor_id, profesor)
    if not updated_profesor:
        raise HTTPException(status_code=404, detail="Profesor not found")
    return updated_profesor

