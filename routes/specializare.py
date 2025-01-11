from fastapi import APIRouter, Depends, HTTPException
from database import SessionLocal

from repository.specializare import (
    create_specializare,
    get_all_specializari,
    get_specializare_by_id,
    update_specializare,
    delete_specializare, get_specializare_by_user_and_facultate
)
from dto.specializare import SpecializareCreate, SpecializareUpdate, SpecializareResponse
from models import User
from auth import get_current_user

router = APIRouter()

# Endpoint pentru a crea o specializare
@router.post("/", response_model=SpecializareResponse)
def create_specializare_route(specializare: SpecializareCreate):
    return create_specializare( specializare)

# Endpoint pentru a obține toate specializările
@router.get("/", response_model=list[SpecializareResponse])
def get_all_specializari_route():
    return get_all_specializari()

# Endpoint pentru a obține o specializare după ID
@router.get("/{id_specializare}", response_model=SpecializareResponse)
def get_specializare_by_id_route(id_specializare: int):
    specializare = get_specializare_by_id(id_specializare)
    if not specializare:
        raise HTTPException(status_code=404, detail="Specializarea nu a fost găsită.")
    return specializare

@router.get("/student/specializare/{id_facultate}", response_model=SpecializareResponse)
def get_specializare_for_facultate(
    id_facultate: int,
    current_user: User = Depends(get_current_user)  # Obține utilizatorul curent
):
    db = SessionLocal()
    try:
        # Obținem specializarea studentului asociată facultății selectate
        specializare = get_specializare_by_user_and_facultate( current_user.id_user, id_facultate)
        if not specializare:
            raise HTTPException(status_code=404, detail="Nu există specializare pentru această facultate.")
        
        return specializare
    finally:
        db.close()

# Endpoint pentru a actualiza o specializare
@router.put("/{id_specializare}", response_model=SpecializareResponse)
def update_specializare_route(id_specializare: int, specializare: SpecializareUpdate):
    updated_specializare = update_specializare( id_specializare, specializare)
    if not updated_specializare:
        raise HTTPException(status_code=404, detail="Specializarea nu a fost găsită.")
    return updated_specializare

# Endpoint pentru a șterge o specializare
@router.delete("/{id_specializare}", response_model=SpecializareResponse)
def delete_specializare_route(id_specializare: int):
    deleted_specializare = delete_specializare( id_specializare)
    if not deleted_specializare:
        raise HTTPException(status_code=404, detail="Specializarea nu a fost găsită.")
    return deleted_specializare
