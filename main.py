from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uvicorn

from database import SessionLocal, engine
import models
from routes import facultati, students, profesori, materii, examene, cereri,useri,grupe

# Crează tabelele în baza de date (dacă nu există deja)
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Grupăm endpoint-urile cu prefixuri specifice
app.include_router(facultati.router, prefix="/facultati", tags=["Facultati"])
app.include_router(students.router, prefix="/students", tags=["Studenti"])
app.include_router(profesori.router, prefix="/profesori", tags=["Profesori"])
app.include_router(materii.router, prefix="/materii", tags=["Materii"])
app.include_router(examene.router, prefix="/examene", tags=["Examene"])
app.include_router(cereri.router, prefix="/cereri", tags=["Cereri"])
app.include_router(useri.router,prefix="/useri",tags=["Useri"])
app.include_router(grupe.router,prefix="/grupe",tags=["Grupe"])
#test
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.2", port=8000)