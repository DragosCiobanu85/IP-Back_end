from fastapi import APIRouter, HTTPException
from typing import List
from dto.sali import SalaCreate, SalaResponse
from repository.sali import insert_sala, get_all_sali, remove_sala

router = APIRouter()

@router.post("/", response_model=SalaResponse)
def create_sala(sala: SalaCreate):
    try:
        return insert_sala(sala)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[SalaResponse])
def read_sali():
    return get_all_sali()

@router.delete("/{sala_id}", response_model=SalaResponse)
def delete_sala(sala_id: int):
    deleted_sala = remove_sala(sala_id)
    if deleted_sala is None:
        raise HTTPException(status_code=404, detail="Sala nu a fost găsită")
    return deleted_sala
