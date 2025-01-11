from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
from dto.useri import UserCreate, UserUpdate

# Funcție pentru a adăuga un user nou
def insert_user(user: UserCreate):
    db = SessionLocal()
    try:
        existing_user = db.query(User).filter(User.email == user.email).first()
        if existing_user:
            raise ValueError("Email-ul există deja în sistem.")
        db_user = User(email=user.email, parola=user.parola, rol=user.rol)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    finally:
        db.close()

# Funcție pentru a obține un user după ID
def get_user_by_id(user_id: int):
    db = SessionLocal()
    try:
        return db.query(User).filter(User.id_user == user_id).first()
    finally:
        db.close()

# Funcție pentru a obține un user după Email
def get_user_by_email(email: str):
    db = SessionLocal()
    try:
        return db.query(User).filter(User.email == email).first()
    finally:
        db.close()

# Funcție pentru a obține toți userii
def get_all_users():
    db = SessionLocal()
    try:
        return db.query(User).all()
    finally:
        db.close()

# Funcție pentru a șterge un user după ID
def delete_user(user_id: int):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id_user == user_id).first()
        if user:
            db.delete(user)
            db.commit()
        return user
    finally:
        db.close()

# Funcție pentru a actualiza un user
def update_user(user_id: int, user_data: UserUpdate):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id_user == user_id).first()
        if not user:
            return None
        if user_data.email:
            user.email = user_data.email
        if user_data.parola:
            user.parola = user_data.parola
        if user_data.rol:
            user.rol = user_data.rol
        db.commit()
        db.refresh(user)
        return user
    finally:
        db.close()
