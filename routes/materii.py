from fastapi import APIRouter, HTTPException
from typing import List
from dto.materii import MaterieCreate, MaterieUpdate, MaterieResponse
from repository.materii import insert_materie, get_all_materii, update_materie, delete_materie
router = APIRouter()
# Endpoint pentru a adăuga o materie
@router.post("/materii/", response_model=MaterieResponse)
def create_materie(materie: MaterieCreate):
    db_materie = insert_materie(materie)
    return db_materie

# Endpoint pentru a obține toate materiile
@router.get("/materii/", response_model=List[MaterieResponse])
def read_materii():
    return get_all_materii()

# Endpoint pentru actualizarea unei materii
@router.put("/materii/{materie_id}", response_model=MaterieResponse)
def update_materie_endpoint(materie_id: int, materie: MaterieUpdate):
    updated_materie = update_materie(materie_id, materie)
    if not updated_materie:
        raise HTTPException(status_code=404, detail="Materie not found")
    return updated_materie

# Endpoint pentru ștergerea unei materii
@router.delete("/materii/{materie_id}", response_model=MaterieResponse)
def delete_materie_endpoint(materie_id: int):
    deleted_materie = delete_materie(materie_id)
    if not deleted_materie:
        raise HTTPException(status_code=404, detail="Materie not found")
    return deleted_materie
