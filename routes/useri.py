from fastapi import APIRouter, HTTPException
from typing import List
from dto.useri import UserResponse, UserCreate, UserUpdate, UserLogin, UserBase
from repository.useri import insert_user, get_user_by_id, get_all_users, delete_user, update_user, get_user_by_email
#from passlib.context import CryptContext

router = APIRouter()

#pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#def hash_password(password: str) -> str:
#   return pwd_context.hash(password)
#de criptat parola - in create_user
# hashed_password = hash_password(user.password)
# user.password = hashed_password  # Înlocuim parola cu cea criptată
@router.post("/users/{login}", response_model=UserLogin)
def login_user(user: UserLogin):  # Accept the UserLogin model from the request body
    user_from_db = get_user_by_email(user.email)
    if not user_from_db or user_from_db.parola != user.parola:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return user_from_db
# Endpoint pentru a adăuga un user nou
@router.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate):
    try:
        db_user = insert_user(user)
        return db_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Endpoint pentru a obține un user după ID


@router.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int):
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Endpoint pentru a obține toți userii
@router.get("/users/", response_model=List[UserResponse])
def read_users():
    return get_all_users()

# Endpoint pentru a șterge un user după ID
@router.delete("/users/{user_id}", response_model=UserResponse)
def remove_user(user_id: int):
    user = delete_user( user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Endpoint pentru a actualiza un user
@router.put("/users/{user_id}", response_model=UserResponse)
def update_user_endpoint(user_id: int, user: UserUpdate):
    updated_user = update_user( user_id, user)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user