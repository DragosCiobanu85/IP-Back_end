from fastapi import APIRouter, Depends, HTTPException
from repository.studenti import (
    get_all_students,
    get_student_by_id,
    insert_student,
    delete_student,
    update_student
)
from dto.studenti import StudentCreate, StudentResponse,StudentUpdate


router = APIRouter()


@router.get("/", response_model=list[StudentResponse])
def read_students():
    students = get_all_students()
    return students


@router.get("/{student_id}", response_model=StudentResponse)
def read_student(student_id: int):
    student = get_student_by_id(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.post("/", response_model=StudentResponse)

def create_student(student: StudentCreate):
    try:
        db_student=insert_student(student)
        return db_student
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{student_id}")
def delete_student_endpoint(student_id: int):
    success = delete_student(student_id)
    if not success:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"detail": "Student deleted successfully"}

@router.put("/{student_id}", response_model=StudentResponse)
def update_student_endpoint(student_id: int, student: StudentUpdate):
    # Actualizăm studentul
    updated_student = update_student(student_id, student)
    if not updated_student:
        raise HTTPException(status_code=404, detail="Student not found")
    return updated_student