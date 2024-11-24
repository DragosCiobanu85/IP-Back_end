from fastapi import APIRouter, Depends, HTTPException
from repository.studenti import (
    get_all_students,
    get_student_by_id,
    insert_student,
    delete_student
)
from dto.studenti import StudentCreate, StudentResponse


router = APIRouter(prefix="/students", tags=["Students"])


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
    print("eror")
    db_student=insert_student(student)
    print("hsdkd")
    return db_student


@router.delete("/{student_id}")
def delete_student_endpoint(student_id: int):
    success = delete_student(student_id)
    if not success:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"detail": "Student deleted successfully"}
