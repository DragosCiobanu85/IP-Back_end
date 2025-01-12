# routes/status.py
from fastapi import APIRouter, HTTPException
from repository.status import create_status, get_all_statusuri, get_status_by_id, update_status, delete_status
from dto.status import StatusCreate, StatusUpdate, StatusResponse

router = APIRouter()

@router.post("/", response_model=StatusResponse)
def create_status_route(status: StatusCreate):
    return create_status(status=status)

@router.get("/", response_model=list[StatusResponse])
def get_all_statusuri_route():
    return get_all_statusuri()

@router.get("/{id_status}", response_model=StatusResponse)
def get_status_route(id_status: int):
    status = get_status_by_id(id_status=id_status)
    if not status:
        raise HTTPException(status_code=404, detail="Status not found")
    return status

@router.put("/{id_status}", response_model=StatusResponse)
def update_status_route(id_status: int, status: StatusUpdate):
    updated_status = update_status(id_status=id_status, status=status)
    if not updated_status:
        raise HTTPException(status_code=404, detail="Status not found")
    return updated_status

@router.delete("/{id_status}", response_model=StatusResponse)
def delete_status_route(id_status: int):
    deleted_status = delete_status(id_status=id_status)
    if not deleted_status:
        raise HTTPException(status_code=404, detail="Status not found")
    return deleted_status
