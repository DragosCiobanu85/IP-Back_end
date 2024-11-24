from fastapi import APIRouter, HTTPException
from typing import List
from dto.cereri import CerereCreate, CerereUpdate, CerereResponse
from repository.cereri import insert_cerere, get_all_cereri, update_cerere, delete_cerere
router = APIRouter()

# Endpoint pentru a adăuga o cerere
@router.post("/cereri/", response_model=CerereResponse)
def create_cerere(cerere: CerereCreate):
    db_cerere = insert_cerere(cerere)
    return db_cerere

# Endpoint pentru a obține toate cererile
@router.get("/cereri/", response_model=List[CerereResponse])
def read_cereri():
    return get_all_cereri()

# Endpoint pentru actualizarea statusului unei cereri
@router.put("/cereri/{cerere_id}", response_model=CerereResponse)
def update_cerere_endpoint(cerere_id: int, cerere: CerereUpdate):
    updated_cerere = update_cerere(cerere_id, cerere)
    if not updated_cerere:
        raise HTTPException(status_code=404, detail="Cerere not found")
    return updated_cerere

# Endpoint pentru ștergerea unei cereri
@router.delete("/cereri/{cerere_id}", response_model=CerereResponse)
def delete_cerere_endpoint(cerere_id: int):
    deleted_cerere = delete_cerere(cerere_id)
    if not deleted_cerere:
        raise HTTPException(status_code=404, detail="Cerere not found")
    return deleted_cerere