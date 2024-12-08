from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
import os
from database import SessionLocal
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from models import User 
# Încărcați variabilele de mediu din fișierul .env
load_dotenv()

# Configurări JWT
SECRET_KEY = os.getenv("SECRET_KEY")  # Cheia secretă citită din fișierul .env
ALGORITHM = os.getenv("ALGORITHM", "HS256")  # Algoritmul de criptare (folosește HS256 ca default)
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))  # Timpul de expirare al tokenului

# Obiect pentru criptarea parolelor
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Obiect OAuth2PasswordBearer pentru extragerea token-ului
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

# --------------------------------------------
# Funcții pentru gestionarea parolelor
# --------------------------------------------

# Verifică dacă parola simplă se potrivește cu parola hash
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Hash-uiește o parolă nouă
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# --------------------------------------------
# Funcții pentru generarea și verificarea token-ului JWT
# --------------------------------------------

# Funcție pentru generarea tokenului JWT
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)  # Timpul de expirare din variabila de mediu
    to_encode.update({"exp": expire})
    print(f"Token data to encode: {to_encode}")
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Funcție pentru a verifica și decoda un token JWT
def verify_token(token: str) -> Optional[str]:
    try:
        payload = jwt.decode(
            token, 
            SECRET_KEY, 
            algorithms=[ALGORITHM], 
            audience="my-app",  # Adaugă un audience pentru validare
            issuer="my-app-server"  # Adaugă un issuer pentru validare
        )
        email: str = payload.get("sub")
        if email is None:
            return None
        return email
    except JWTError:
        return None

# --------------------------------------------
# Funcție pentru a obține utilizatorul curent
# --------------------------------------------


def get_user_by_email( email: str):
    db=SessionLocal()
    """
    Căutăm un utilizator în baza de date după email.
    """
    return db.query(User).filter(User.email == email).first()

def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """
    Verifică token-ul JWT și returnează un obiect User.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, 
            SECRET_KEY, 
            algorithms=[ALGORITHM]
        )
        email: str = payload.get("sub")
        rol: str = payload.get("rol")

        if email is None or rol is None:
            raise credentials_exception

        # Căutăm utilizatorul în baza de date
        user = get_user_by_email(email)

        if user is None:
            raise credentials_exception

        return user  # Returnează un obiect User

    except JWTError:
        raise credentials_exception

    
def get_current_user_id(token: str = Depends(oauth2_scheme)) -> str:
    try:
        # Decodifică token-ul JWT pentru a extrage datele
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        
        # Verifică dacă token-ul este expirat
        if payload["exp"] < datetime.utcnow().timestamp():
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is expired")
        
        # Returnează sub (email-ul utilizatorului) sau un alt identificator unic
        return payload["sub"]
    
    except jwt.JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

