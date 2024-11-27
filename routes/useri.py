from fastapi import APIRouter, HTTPException
from typing import List
from dto.useri import UserResponse, UserCreate, UserUpdate
from repository.useri import insert_user, get_user_by_id, get_all_users, delete_user, update_user

router = APIRouter()

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
