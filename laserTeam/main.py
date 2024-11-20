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

from dto.materii import MaterieCreate, MaterieUpdate, MaterieResponse
from repository.materii import insert_materie, get_all_materii, update_materie, delete_materie

from dto.useri import UserResponse, UserCreate, UserUpdate
from repository.useri import insert_user, get_user_by_id, get_all_users, delete_user, update_user

from dto.cereri import CerereCreate, CerereUpdate, CerereResponse
from repository.cereri import insert_cerere, get_all_cereri, update_cerere, delete_cerere

from dto.examene import ExamenCreate, ExamenUpdate, ExamenResponse
from repository.examene import insert_examen, get_all_examene, update_examen, delete_examen




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

#---------Materii----------
# Endpoint pentru a adăuga o materie
@app.post("/materii/", response_model=MaterieResponse)
def create_materie(materie: MaterieCreate):
    db_materie = insert_materie(materie)
    return db_materie

# Endpoint pentru a obține toate materiile
@app.get("/materii/", response_model=List[MaterieResponse])
def read_materii():
    return get_all_materii()

# Endpoint pentru actualizarea unei materii
@app.put("/materii/{materie_id}", response_model=MaterieResponse)
def update_materie_endpoint(materie_id: int, materie: MaterieUpdate):
    updated_materie = update_materie(materie_id, materie)
    if not updated_materie:
        raise HTTPException(status_code=404, detail="Materie not found")
    return updated_materie

# Endpoint pentru ștergerea unei materii
@app.delete("/materii/{materie_id}", response_model=MaterieResponse)
def delete_materie_endpoint(materie_id: int):
    deleted_materie = delete_materie(materie_id)
    if not deleted_materie:
        raise HTTPException(status_code=404, detail="Materie not found")
    return deleted_materie


#----------User------------
# Endpoint pentru a adăuga un user nou
@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(SessionLocal)):
    db_user = insert_user(db, user)
    return db_user

# Endpoint pentru a obține un user după ID
@app.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(SessionLocal)):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Endpoint pentru a obține toți userii
@app.get("/users/", response_model=List[UserResponse])
def read_users(db: Session = Depends(SessionLocal)):
    return get_all_users(db)

# Endpoint pentru a șterge un user după ID
@app.delete("/users/{user_id}", response_model=UserResponse)
def remove_user(user_id: int, db: Session = Depends(SessionLocal)):
    user = delete_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Endpoint pentru a actualiza un user
@app.put("/users/{user_id}", response_model=UserResponse)
def update_user_endpoint(user_id: int, user: UserUpdate, db: Session = Depends(SessionLocal)):
    updated_user = update_user(db, user_id, user)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

#------------Cerere-------------
# Endpoint pentru a adăuga o cerere
@app.post("/cereri/", response_model=CerereResponse)
def create_cerere(cerere: CerereCreate):
    db_cerere = insert_cerere(cerere)
    return db_cerere

# Endpoint pentru a obține toate cererile
@app.get("/cereri/", response_model=List[CerereResponse])
def read_cereri():
    return get_all_cereri()

# Endpoint pentru actualizarea statusului unei cereri
@app.put("/cereri/{cerere_id}", response_model=CerereResponse)
def update_cerere_endpoint(cerere_id: int, cerere: CerereUpdate):
    updated_cerere = update_cerere(cerere_id, cerere)
    if not updated_cerere:
        raise HTTPException(status_code=404, detail="Cerere not found")
    return updated_cerere

# Endpoint pentru ștergerea unei cereri
@app.delete("/cereri/{cerere_id}", response_model=CerereResponse)
def delete_cerere_endpoint(cerere_id: int):
    deleted_cerere = delete_cerere(cerere_id)
    if not deleted_cerere:
        raise HTTPException(status_code=404, detail="Cerere not found")
    return deleted_cerere

#------Examen---------
# Endpoint pentru a adăuga un examen
@app.post("/examene/", response_model=ExamenResponse)
def create_examen(examen: ExamenCreate):
    db_examen = insert_examen(examen)
    return db_examen


# Endpoint pentru a obține toate examenele
@app.get("/examene/", response_model=List[ExamenResponse])
def read_examene():
    return get_all_examene()


# Endpoint pentru actualizarea unui examen
@app.put("/examene/{examen_id}", response_model=ExamenResponse)
def update_examen_endpoint(examen_id: int, examen: ExamenUpdate):
    updated_examen = update_examen(examen_id, examen)
    if not updated_examen:
        raise HTTPException(status_code=404, detail="Examen not found")
    return updated_examen


# Endpoint pentru ștergerea unui examen
@app.delete("/examene/{examen_id}", response_model=ExamenResponse)
def delete_examen_endpoint(examen_id: int):
    deleted_examen = delete_examen(examen_id)
    if not deleted_examen:
        raise HTTPException(status_code=404, detail="Examen not found")
    return deleted_examen