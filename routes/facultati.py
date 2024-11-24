from fastapi import APIRouter, HTTPException
from typing import List
from dto.facultati import FacultateCreate, FacultateResponse
from repository.facultati import insert_faculate, get_all_facultati, remove_facultate

router = APIRouter()

@router.post("/", response_model=FacultateResponse)
def create_facultate(facultate: FacultateCreate):
    print("jnfmd")
    return insert_faculate(facultate)

@router.get("/", response_model=List[FacultateResponse])
def read_facultati():
    return get_all_facultati()

@router.delete("/{facultate_id}", response_model=FacultateResponse)
def delete_facultate(facultate_id: int):
    deleted_facultate = remove_facultate(facultate_id)
    if deleted_facultate is None:
        raise HTTPException(status_code=404, detail="Facultatea nu a fost găsită")
    return deleted_facultate
