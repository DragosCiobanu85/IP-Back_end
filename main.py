from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uvicorn
from fastapi.middleware.cors import CORSMiddleware  # Adăugăm importul pentru CORS

from database import SessionLocal, engine
import models
from routes import facultati, studenti, profesori, materii, examene, cereri, useri, grupe, sali

# Crează tabelele în baza de date (dacă nu există deja)
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Definirea originilor permise pentru frontend
origins = [
    "http://localhost:3000",  # frontend-ul tău, de exemplu http://localhost:3000
]

# Adăugarea middleware-ului CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite cereri doar de la acest frontend
    allow_credentials=True,
    allow_methods=["*"],  # Permite toate metodele HTTP
    allow_headers=["*"],  # Permite toate antetele
)

# Grupăm endpoint-urile cu prefixuri specifice
app.include_router(facultati.router, prefix="/facultati", tags=["Facultati"])
app.include_router(studenti.router, prefix="/studenti", tags=["Studenti"])
app.include_router(profesori.router, prefix="/profesori", tags=["Profesori"])
app.include_router(materii.router, prefix="/materii", tags=["Materii"])
app.include_router(examene.router, prefix="/examene", tags=["Examene"])
app.include_router(cereri.router, prefix="/cereri", tags=["Cereri"])
app.include_router(useri.router, prefix="/useri", tags=["Useri"])
app.include_router(grupe.router, prefix="/grupe", tags=["Grupe"])
app.include_router(sali.router, prefix="/sali", tags=["Sali"])

# Test: rulează aplicația FastAPI
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
