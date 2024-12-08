from fastapi import APIRouter, HTTPException, Depends
from datetime import timedelta
from auth import verify_password, create_access_token, get_password_hash, ACCESS_TOKEN_EXPIRE_MINUTES
from repository.useri import get_user_by_email
from dto.useri import UserResponse, UserCreate, UserUpdate, UserLogin, UserBase
from repository.useri import insert_user, get_user_by_id, get_all_users, delete_user, update_user, get_user_by_email
from repository.profesori import get_profesor_by_user_id
from repository.studenti import get_student_by_user_id
from typing import List
from dto.useri import UserLogin
from auth import get_current_user
from database import SessionLocal

router = APIRouter()

@router.post("/users/login")
def login_user(user: UserLogin):
    db=SessionLocal
    # Căutăm utilizatorul în baza de date după email
    user_from_db = get_user_by_email(user.email)
    if not user_from_db or not verify_password(user.parola, user_from_db.parola):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # Identificăm id-ul utilizatorului și rolul
    user_id = user_from_db.id_user
    user_role = user_from_db.rol
    
    # Căutăm detaliile asociate rolului utilizatorului
    if user_role == "Profesor":
        profesor = get_profesor_by_user_id( user_id)
        if not profesor:
            raise HTTPException(status_code=404, detail="Profesor not found")
        user_details = {"id": profesor.id_Profesor, "name": profesor.nume, "rol": "Profesor"}
    elif user_role == "Student":
        student = get_student_by_user_id( user_id)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        user_details = {"id": student.id_Student, "name": student.nume, "rol": "Student"}
    else:
        raise HTTPException(status_code=400, detail="Invalid role")
    
    # Generare token JWT cu rolul utilizatorului și detalii suplimentare
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_from_db.email, "rol": user_role, "user_details": user_details},  # Adăugăm detalii în payload
        expires_delta=access_token_expires
    )

    return {"message": "Login successful", "access_token": access_token, "token_type": "bearer"}



@router.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate):
    # Verificăm dacă un utilizator cu acest email există deja
    existing_user = get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Criptăm parola înainte de a o salva în DB
    hashed_password = get_password_hash(user.parola)
    user.parola = hashed_password  # Înlocuim parola originală cu cea criptată
    
    try:
        db_user = insert_user(user)
        return db_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int, current_user: str = Depends(get_current_user)):
    # Verificăm dacă utilizatorul există
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/users/", response_model=List[UserResponse])
def read_users(current_user: str = Depends(get_current_user)):
    # Returnează toți utilizatorii
    return get_all_users()

@router.delete("/users/{user_id}", response_model=UserResponse)
def remove_user(user_id: int, current_user: str = Depends(get_current_user)):
    # Ștergem utilizatorul din baza de date
    user = delete_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/users/{user_id}", response_model=UserResponse)
def update_user_endpoint(user_id: int, user: UserUpdate, current_user: str = Depends(get_current_user)):
    # Actualizăm utilizatorul în baza de date
    updated_user = update_user(user_id, user)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user
