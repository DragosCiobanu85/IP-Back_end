# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL-ul de conexiune la baza de date (din alembic.ini)
DATABASE_URL = "mssql+pyodbc://@localhost/laserteam?driver=ODBC+Driver+17+for+SQL+Server"

# Crearea unui engine SQLAlchemy
engine = create_engine(DATABASE_URL)

# Crearea unei clase SessionLocal pentru a gestiona sesiunile de DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declararea bazei pentru toate modelele
Base = declarative_base()
