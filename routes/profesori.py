from fastapi import APIRouter, HTTPException
from typing import List
from dto.profesori import ProfesorResponse, ProfesorCreate, ProfesorUpdate
from repository.profesori import insert_profesor, get_all_profesori, delete_profesor, update_profesor

router = APIRouter()
#----------Profesori---------------

# Endpoint pentru a adăuga un profesor
@router.post("/profesori/", response_model=ProfesorResponse)
def create_profesor(profesor: ProfesorCreate):
    try:
        db_profesor = insert_profesor(profesor)
        return db_profesor
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Endpoint pentru a obține toți profesorii
@router.get("/profesori/", response_model=List[ProfesorResponse])
def read_profesori():
    return get_all_profesori()

# Endpoint pentru a șterge un profesor după ID
@router.delete("/profesori/{profesor_id}", response_model=ProfesorResponse)
def delete_profesor_endpoint(profesor_id: int):
    profesor = delete_profesor(profesor_id)
    if not profesor:
        raise HTTPException(status_code=404, detail="Profesor not found")
    return profesor

# Endpoint pentru a actualiza un profesor
@router.put("/profesori/{profesor_id}", response_model=ProfesorResponse)
def update_profesor_endpoint(profesor_id: int, profesor: ProfesorUpdate):
    updated_profesor = update_profesor(profesor_id, profesor)
    if not updated_profesor:
        raise HTTPException(status_code=404, detail="Profesor not found")
    return updated_profesor