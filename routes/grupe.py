from fastapi import APIRouter, HTTPException
from typing import List
from dto.grupe import GrupaResponse, GrupaCreate, GrupaUpdate
from repository.grupe import insert_grupa, get_grupa_by_id, get_all_grupe, delete_grupa, update_grupa
router = APIRouter()
# Endpoint pentru a adăuga o grupă nouă
@router.post("/grupe/", response_model=GrupaResponse)
def create_grupa(grupa: GrupaCreate):
    try:
        db_grupa = insert_grupa(grupa)
        return db_grupa
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Endpoint pentru a obține o grupă după ID
@router.get("/grupe/{grupa_id}", response_model=GrupaResponse)
def read_grupa(grupa_id: int):
    grupa = get_grupa_by_id(grupa_id)
    if not grupa:
        raise HTTPException(status_code=404, detail="Grupa not found")
    return grupa

# Endpoint pentru a obține toate grupele
@router.get("/grupe/", response_model=List[GrupaResponse])
def read_grupe():
    return get_all_grupe()

# Endpoint pentru a șterge o grupă după ID
@router.delete("/grupe/{grupa_id}", response_model=GrupaResponse)
def remove_grupa(grupa_id: int):
    grupa = delete_grupa(grupa_id)
    if not grupa:
        raise HTTPException(status_code=404, detail="Grupa not found")
    return grupa

# Endpoint pentru a actualiza o grupă
@router.put("/grupe/{grupa_id}", response_model=GrupaResponse)
def update_grupa_endpoint(grupa_id: int, grupa: GrupaUpdate):
    updated_grupa = update_grupa(grupa_id, grupa)
    if not updated_grupa:
        raise HTTPException(status_code=404, detail="Grupa not found")
    return updated_grupa