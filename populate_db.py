from sqlalchemy.orm import Session
from database import engine  # Asigură-te că engine-ul e definit corect
from models import Facultate, Grupa, Student, User, Profesor, Sala, Materie  # Importă modelele

# Datele facultăților
facultati = [
    {"id_Facultate": 1, "nume": "FIESC"},
    {"id_Facultate": 2, "nume": "FIMAR"},
    {"id_Facultate": 3, "nume": "FEFS"},
    {"id_Facultate": 4, "nume": "FIA"},
    {"id_Facultate": 5, "nume": "FIG"},
    {"id_Facultate": 6, "nume": "FLSC"},
    {"id_Facultate": 7, "nume": "FS"},
    {"id_Facultate": 8, "nume": "FEAA"},
    {"id_Facultate": 9, "nume": "FSE"},
    {"id_Facultate": 10, "nume": "FDSA"},
    {"id_Facultate": 20, "nume": "DSPP"},
    {"id_Facultate": 21, "nume": "FMSB"},
    {"id_Facultate": 22, "nume": "CSUD"},
]

# Datele grupelor
grupe = {
    1: ["3211", "3212", "3213", "3214", "3221", "3231", "3241", "3111", "3112", "3141", "3142", "3143", "3144"],
    2: ["4511", "4521", "4531", "4541"],
}

users = [
    {"email": "ion.popescu@student.usv.ro", "parola": "Ion1234", "rol": "Student", "nume": "Popescu", "prenume": "Ion"},
    {"email": "maria.ionescu@student.usv.ro", "parola": "Maria1234", "rol": "Student", "nume": "Ionescu", "prenume": "Maria"},
    {"email": "george.mihailescu@student.usv.ro", "parola": "George1234", "rol": "Student", "nume": "Mihailescu", "prenume": "George"},
    {"email": "adina.tanase@student.usv.ro", "parola": "Adina1234", "rol": "Student", "nume": "Tanase", "prenume": "Adina"},
    {"email": "andrei.stanescu@student.usv.ro", "parola": "Andrei1234", "rol": "Student", "nume": "Stanescu", "prenume": "Andrei"},
    {"email": "ioana.bucur@student.usv.ro", "parola": "Ioana1234", "rol": "Student", "nume": "Bucur", "prenume": "Ioana"},
    {"email": "marian.dumitru@student.usv.ro", "parola": "Marian1234", "rol": "Student", "nume": "Dumitru", "prenume": "Marian"},
    {"email": "lidia.popa@student.usv.ro", "parola": "Lidia1234", "rol": "Student", "nume": "Popa", "prenume": "Lidia"},
    {"email": "cosmin.sandu@student.usv.ro", "parola": "Cosmin1234", "rol": "Student", "nume": "Sandu", "prenume": "Cosmin"},
    {"email": "elena.vasilescu@student.usv.ro", "parola": "Elena1234", "rol": "Student", "nume": "Vasilescu", "prenume": "Elena"},
    {"email": "mihai.radu@usm.ro", "parola": "Mihai1234", "rol": "Profesor", "nume": "Radu", "prenume": "Mihai"},
    {"email": "andra.popescu@usm.ro", "parola": "Andra1234", "rol": "Profesor", "nume": "Popescu", "prenume": "Andra"},
    {"email": "daniel.marin@usm.ro", "parola": "Daniel1234", "rol": "Profesor", "nume": "Marin", "prenume": "Daniel"},
]

students = [
    {"nume": "Popescu", "prenume": "Ion", "id_Grupa": 3141, "user_email": "ion.popescu@student.usv.ro"},
    {"nume": "Ionescu", "prenume": "Maria", "id_Grupa": 3141, "user_email": "maria.ionescu@student.usv.ro"},
    {"nume": "Mihailescu", "prenume": "George", "id_Grupa": 3142, "user_email": "george.mihailescu@student.usv.ro"},
    {"nume": "Tanase", "prenume": "Adina", "id_Grupa": 3142, "user_email": "adina.tanase@student.usv.ro"},
    {"nume": "Stanescu", "prenume": "Andrei", "id_Grupa": 3142, "user_email": "andrei.stanescu@student.usv.ro"},
    {"nume": "Bucur", "prenume": "Ioana", "id_Grupa": 3142, "user_email": "ioana.bucur@student.usv.ro"},
    {"nume": "Dumitru", "prenume": "Marian", "id_Grupa": 3143, "user_email": "marian.dumitru@student.usv.ro"},
    {"nume": "Popa", "prenume": "Lidia", "id_Grupa": 3143, "user_email": "lidia.popa@student.usv.ro"},
    {"nume": "Sandu", "prenume": "Cosmin", "id_Grupa": 3143, "user_email": "cosmin.sandu@student.usv.ro"},
    {"nume": "Vasilescu", "prenume": "Elena", "id_Grupa": 3144, "user_email": "elena.vasilescu@student.usv.ro"},
]

professors_data = [
    {"nume": "Radu", "prenume": "Mihai", "id_Facultate": 1, "user_email": "mihai.radu@usm.ro", "grad": "Profesor"},
    {"nume": "Popescu", "prenume": "Andra", "id_Facultate": 1, "user_email": "andra.popescu@usm.ro", "grad": "Lector"},
    {"nume": "Marin", "prenume": "Daniel", "id_Facultate": 1, "user_email": "daniel.marin@usm.ro", "grad": "Asistent"},
]
sali_data = [
    {"nume": "C001"},
    {"nume": "C002"},
    {"nume": "C003"},
    {"nume": "C004"},
    {"nume": "C005"},
    {"nume": "C006"},
    {"nume": "C007"},
    {"nume": "C008"},
    {"nume": "C009"},
    {"nume": "C010"},
    {"nume": "C101"},
    {"nume": "C102"},
    {"nume": "C103"},
    {"nume": "C104"},
    {"nume": "C105"},
    {"nume": "C106"},
    {"nume": "C107"},
    {"nume": "C108"},
    {"nume": "C109"},
    {"nume": "C201"},
    {"nume": "C202"},
    {"nume": "C203"},
    {"nume": "C204"},
    {"nume": "C205"},
    {"nume": "C206"},
    {"nume": "C207"},
    {"nume": "C208"},
    {"nume": "C209"},
]

materii_data = [
    {"nume": "PrT", "tip_examen": "scris", "an_studiu": 1, "semestru": 1},
    {"nume": "CMo", "tip_examen": "oral", "an_studiu": 1, "semestru": 2},
    {"nume": "IP", "tip_examen": "moodle", "an_studiu": 2, "semestru": 3},
    {"nume": "SIEP", "tip_examen": "practic", "an_studiu": 2, "semestru": 4},
    {"nume": "PBD", "tip_examen": "scris", "an_studiu": 3, "semestru": 5},
    {"nume": "MS", "tip_examen": "oral", "an_studiu": 3, "semestru": 6},
    {"nume": "Fizica1", "tip_examen": "moodle", "an_studiu": 1, "semestru": 1},
    {"nume": "Fizica2", "tip_examen": "scris", "an_studiu": 1, "semestru": 2},
    {"nume": "PACME", "tip_examen": "practic", "an_studiu": 2, "semestru": 3},
    {"nume": "SCTR", "tip_examen": "oral", "an_studiu": 2, "semestru": 4},
    {"nume": "MN", "tip_examen": "scris", "an_studiu": 3, "semestru": 5},
    {"nume": "GAC", "tip_examen": "moodle", "an_studiu": 3, "semestru": 6},
    {"nume": "PCLP", "tip_examen": "practic", "an_studiu": 1, "semestru": 1},
    {"nume": "POO", "tip_examen": "oral", "an_studiu": 2, "semestru": 3},
    {"nume": "SDA", "tip_examen": "scris", "an_studiu": 2, "semestru": 4},
    {"nume": "PAlg", "tip_examen": "moodle", "an_studiu": 1, "semestru": 2},
]

# Funcțiile pentru popularea fiecărui tabel

def populate_facultati(session):
    for fac in facultati:
        facultate = Facultate(id_Facultate=fac["id_Facultate"], nume=fac["nume"])
        session.add(facultate)

def populate_grupe(session):
    for id_facultate, nume_grupe in grupe.items():
        for nume_grupa in nume_grupe:
            grupa = Grupa(nume=nume_grupa, id_Facultate=id_facultate)
            session.add(grupa)
    session.flush()

def populate_users(session):
    for user_data in users:
        user = User(
            email=user_data["email"],
            parola=user_data["parola"],
            rol=user_data["rol"]
        )
        session.add(user)


def populate_students(session):
    for student_data in students:
        # Căutăm utilizatorul pe baza email-ului
        user = session.query(User).filter_by(email=student_data["user_email"]).first()

        if user:
            # Căutăm grupa după numele acesteia
            grupa = session.query(Grupa).filter_by(nume=student_data["id_Grupa"]).first()

            if grupa:
                # Creăm studentul folosind id-ul grupei
                student = Student(
                    nume=student_data["nume"],
                    prenume=student_data["prenume"],
                    id_Grupa=grupa.id_Grupa,  # Folosim id-ul grupei găsite
                    id_user=user.id_user  # Asociem studentul cu utilizatorul
                )
                session.add(student)
            else:
                print(
                    f"Grupa {student_data['id_Grupa']} nu a fost găsită pentru studentul {student_data['nume']} {student_data['prenume']}")

def populate_professors(session):
    for professor_data in professors_data:
        user = session.query(User).filter_by(email=professor_data["user_email"]).first()
        if user:
            professor = Profesor(
                nume=professor_data["nume"],
                prenume=professor_data["prenume"],
                grad=professor_data["grad"],
                id_Facultate=professor_data["id_Facultate"],
                id_user=user.id_user
            )
            session.add(professor)

def populate_sali(session):
    # Parcurgem lista salilor și adăugăm fiecare în sesiunea curentă
    for sala_data in sali_data:
        sala = Sala(nume=sala_data["nume"])
        session.add(sala)
    session.commit()


def populate_materii(session):
    # Obține lista profesorilor existenți în baza de date
    profesori = session.query(Profesor).all()
    if not profesori:
        print("Nu există profesori în baza de date! Adaugă profesori înainte de a popula materiile.")
        return

    profesor_ids = [profesor.id_Profesor for profesor in profesori]

    for idx, materie_data in enumerate(materii_data):
        # Alege un profesor din listă în mod secvențial (circular, dacă numărul e mai mare decât profesorii disponibili)
        profesor_id = profesor_ids[idx % len(profesor_ids)]

        # Creează obiectul Materie
        materie = Materie(
            nume=materie_data["nume"],
            id_Profesor=profesor_id,
            tip_examen=materie_data["tip_examen"],
            an_studiu=materie_data["an_studiu"],
            semestru=materie_data["semestru"]
        )
        session.add(materie)

    session.commit()

# Funcția principală care va apela funcțiile pentru fiecare tabel
def populate():
    with Session(engine) as session:
        # Șterge datele existente pentru o populare curată (opțional)
        session.query(Materie).delete()
        session.query(Sala).delete()
        session.query(Student).delete()
        session.query(Profesor).delete()
        session.query(User).delete()
        session.query(Grupa).delete()
        session.query(Facultate).delete()

        session.commit()

        # Populează fiecare tabel
        populate_facultati(session)
        populate_grupe(session)
        populate_users(session)

        populate_students(session)
        populate_professors(session)
        populate_sali(session)
        populate_materii(session)

        session.commit()
        print("Baza de date populată cu succes!")

# Rulează popularea dacă fișierul este executat direct
if __name__ == "__main__":
    populate()
