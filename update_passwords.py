from database import SessionLocal
from auth import get_password_hash
from repository.useri import get_all_users, update_user

# Creează o sesiune cu baza de date
db = SessionLocal()

# Obține toți utilizatorii din baza de date
for user in get_all_users():
    # Verifică dacă parola nu este deja criptată corect (prefixul pentru bcrypt)
    if not user.parola.startswith("$2b$"):
        # Criptează parola utilizatorului
        user.parola = get_password_hash(user.parola)

        # Actualizează utilizatorul în baza de date
        update_user(user.id_user, user)

print("Parolele au fost actualizate cu succes.")
