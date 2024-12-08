from sqlalchemy.orm import Session
from database import SessionLocal
from fastapi import APIRouter, HTTPException
from fastapi import Depends
from auth import get_current_user_id, get_current_user
from models import Cerere, Profesor, User, Student, Grupa
from dto.cereri import CerereCreate, CerereUpdate
from repository.profesori import get_profesor_by_user_id
from repository.studenti import get_student_by_user_id

# Funcție pentru a adăuga o cerere nouă
def insert_cerere(cerere: CerereCreate, current_user: User = Depends(get_current_user)):
    db = SessionLocal()
    try:
        # Obține studentul pe baza id_user (acesta este un user logat, deci va fi student dacă este cazul)
        student = get_student_by_user_id(current_user)

        # Verifică dacă studentul există
        if not student:
            raise HTTPException(status_code=404, detail="Studentul nu a fost găsit.")

        # Crează cererea și autocomplează id_Student
        db_cerere = Cerere(
            id_Profesor=cerere.id_Profesor,
            id_Facultate=cerere.id_Facultate,
            id_Student=student.id_Student,
            id_Grupa= student.id_Grupa,  # Completează automat id_Student
            id_Materie=cerere.id_Materie,
            data=cerere.data,
        )

        db.add(db_cerere)
        db.commit()
        db.refresh(db_cerere)
        return db_cerere
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


# Funcție pentru a obține toate cererile
def get_all_cereri(current_user_email: str = None):
    db = SessionLocal()  # Inițializarea sesiunii DB
    try:
        if current_user_email:
            # Căutăm utilizatorul pe baza email-ului
            user_from_db = db.query(User).filter(User.email == current_user_email).first()
            
            if user_from_db:
                user_id = user_from_db.id_user
                rol = user_from_db.rol
                
                # În funcție de rolul utilizatorului, căutăm profesorul sau studentul
                if rol == "Profesor":
                    # Căutăm profesorul pe baza id_user
                    profesor = get_profesor_by_user_id(user_id)
                    if profesor:
                        # Dacă profesorul este găsit, folosim id-ul profesorului pentru a filtra cererile
                        cereri = db.query(Cerere).filter(Cerere.id_Profesor == profesor.id_Profesor).all()
                    else:
                        cereri = []
                        print(f"Profesor cu email-ul {current_user_email} nu a fost găsit.")
                elif rol == "Student":
                    # Dacă rolul este student, căutăm studentul și filtrăm cererile pentru student
                    student = get_student_by_user_id(user_id)
                    if student:
                        cereri = db.query(Cerere).filter(Cerere.id_Student == student.id_Student).all()
                    else:
                        cereri = []
                        print(f"Student cu email-ul {current_user_email} nu a fost găsit.")
                else:
                    cereri = []  # Dacă rolul nu este nici profesor, nici student
                    print(f"Rolul {rol} nu este valid pentru {current_user_email}.")
            else:
                cereri = []
                print(f"Utilizatorul cu email-ul {current_user_email} nu a fost găsit.")
        else:
            # Dacă nu există un email (de exemplu, pentru admin), returnăm toate cererile
            cereri = db.query(Cerere).all()

        return cereri
    finally:
        db.close()  # Închide sesiunea DB


def update_cerere(cerere_id: int, cerere_data: CerereUpdate, current_user: User = Depends(get_current_user)):
    db = SessionLocal()
    try:
        # Obține studentul pe baza id_user (autentificat)
        student = get_student_by_user_id(current_user)
        
        # Verifică dacă studentul există
        if not student:
            raise HTTPException(status_code=404, detail="Studentul nu a fost găsit pentru acest utilizator.")
        print(f"Student găsit: ID Student = {student.id_Student}, ID Grupă = {student.id_Grupa}")
        
        # Verifică dacă grupa există
        grupa = db.query(Grupa).filter(Grupa.id_Grupa == student.id_Grupa).first()
        if not grupa:
            raise HTTPException(status_code=404, detail="Grupa nu a fost găsită pentru acest student.")
        print(f"Grupă găsită: ID Grupă = {grupa.id_Grupa}")
        
        # Caută cererea în baza de date
        cerere = db.query(Cerere).filter(Cerere.id_Cerere == cerere_id).first()
        if not cerere:
            raise HTTPException(status_code=404, detail=f"Cererea cu ID-ul {cerere_id} nu a fost găsită.")
        print(f"Cerere găsită înainte de actualizare: {cerere.__dict__}")

        # Actualizează câmpurile cererii
        cerere.id_Facultate = cerere_data.id_Facultate
        cerere.id_Profesor = cerere_data.id_Profesor
        cerere.id_Materie = cerere_data.id_Materie
        cerere.id_Student = student.id_Student  # Autocompletare automată
        cerere.id_Grupa = grupa.id_Grupa        # Autocompletare automată
        cerere.data = cerere_data.data

        # Salvează modificările
        db.commit()
        db.refresh(cerere)
        print(f"Cerere actualizată cu succes: {cerere.__dict__}")
        
        return cerere
    
    except Exception as e:
        db.rollback()  # Revoc modificările în caz de eroare
        print(f"Eroare neașteptată: {e}")
        raise HTTPException(status_code=500, detail="A apărut o eroare internă în timpul actualizării cererii.")
    
    finally:
        db.close()
        print("Conexiunea la baza de date a fost închisă.")




# Funcție pentru ștergerea unei cereri
def delete_cerere(cerere_id: int):
    db = SessionLocal()
    try:
        cerere = db.query(Cerere).filter(Cerere.id_Cerere == cerere_id).first()
        if not cerere:
            return None
        db.delete(cerere)
        db.commit()
        return cerere
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()
