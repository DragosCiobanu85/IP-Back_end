from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from repository.an_studiu import (
    create_an_studiu,
    get_all_ani_studiu,
    get_an_studiu_by_id,
    update_an_studiu,
    delete_an_studiu,
)
from dto.an_studiu import AnStudiuCreate, AnStudiuUpdate, AnStudiuResponse

router = APIRouter()

# Endpoint pentru a crea un an de studiu
@router.post("/", response_model=AnStudiuResponse)
def create_an_studiu_route(an_studiu: AnStudiuCreate):
    return create_an_studiu(an_studiu)

# Endpoint pentru a obține toți anii de studiu
@router.get("/", response_model=list[AnStudiuResponse])
def get_all_ani_studiu_route():
    return get_all_ani_studiu()

# Endpoint pentru a obține un an de studiu după ID
@router.get("/{id_an_studiu}", response_model=AnStudiuResponse)
def get_an_studiu_by_id_route(id_an_studiu: int):
    an_studiu = get_an_studiu_by_id( id_an_studiu)
    if not an_studiu:
        raise HTTPException(status_code=404, detail="Anul de studiu nu a fost găsit.")
    return an_studiu

# Endpoint pentru a actualiza un an de studiu
@router.put("/{id_an_studiu}", response_model=AnStudiuResponse)
def update_an_studiu_route(id_an_studiu: int, an_studiu: AnStudiuUpdate):
    updated_an_studiu = update_an_studiu(id_an_studiu, an_studiu)
    if not updated_an_studiu:
        raise HTTPException(status_code=404, detail="Anul de studiu nu a fost găsit.")
    return updated_an_studiu

# Endpoint pentru a șterge un an de studiu
@router.delete("/{id_an_studiu}", response_model=AnStudiuResponse)
def delete_an_studiu_route(id_an_studiu: int):
    deleted_an_studiu = delete_an_studiu( id_an_studiu)
    if not deleted_an_studiu:
        raise HTTPException(status_code=404, detail="Anul de studiu nu a fost găsit.")
    return deleted_an_studiu
