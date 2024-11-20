from sqlalchemy.orm import Session
from models import User
from dto.useri import UserCreate, UserUpdate

# Funcție pentru a adăuga un user nou
def insert_user(db: Session, user: UserCreate):
    db_user = User(email=user.email, parola=user.parola, rol=user.rol)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Funcție pentru a obține un user după ID
def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id_user == user_id).first()

# Funcție pentru a obține toți userii
def get_all_users(db: Session):
    return db.query(User).all()

# Funcție pentru a șterge un user după ID
def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id_user == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    return user

# Funcție pentru a actualiza un user
def update_user(db: Session, user_id: int, user_data: UserUpdate):
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
