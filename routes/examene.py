from fastapi import APIRouter, HTTPException
from typing import List
from dto.examene import ExamenCreate, ExamenUpdate, ExamenResponse
from repository.examene import insert_examen, get_all_examene, update_examen, delete_examen

router = APIRouter()
# Endpoint pentru a adăuga un examen
@router.post("/examene/", response_model=ExamenResponse)
def create_examen(examen: ExamenCreate):
    db_examen = insert_examen(examen)
    return db_examen


# Endpoint pentru a obține toate examenele
@router.get("/examene/", response_model=List[ExamenResponse])
def read_examene():
    return get_all_examene()


# Endpoint pentru actualizarea unui examen
@router.put("/examene/{examen_id}", response_model=ExamenResponse)
def update_examen_endpoint(examen_id: int, examen: ExamenUpdate):
    updated_examen = update_examen(examen_id, examen)
    if not updated_examen:
        raise HTTPException(status_code=404, detail="Examen not found")
    return updated_examen


# Endpoint pentru ștergerea unui examen
@router.delete("/examene/{examen_id}", response_model=ExamenResponse)
def delete_examen_endpoint(examen_id: int):
    deleted_examen = delete_examen(examen_id)
    if not deleted_examen:
        raise HTTPException(status_code=404, detail="Examen not found")
    return deleted_examen