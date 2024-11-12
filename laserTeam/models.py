from sqlalchemy import Column, Integer, String, ForeignKey, Date, Time
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.dialects.mssql import VARCHAR

# Declaring Base
Base = declarative_base()

# Facultate Table
class Facultate(Base):
    __tablename__ = 'Facultate'
    id_Facultate = Column(Integer, primary_key=True, autoincrement=True)
    nume = Column(VARCHAR(100), nullable=False)

# User Table
class User(Base):
    __tablename__ = 'User'
    id_user = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(VARCHAR(100), nullable=False, unique=True)
    parola = Column(VARCHAR(50), nullable=False)
    rol = Column(VARCHAR(20), nullable=False)  # Role can be 'Student' or 'Profesor'

# Student Table
class Student(Base):
    __tablename__ = 'Student'
    id_Student = Column(Integer, primary_key=True, autoincrement=True)
    nume = Column(VARCHAR(50), nullable=False)
    prenume = Column(VARCHAR(50), nullable=False)
    grupa = Column(VARCHAR(10), nullable=False, unique=True)  # Make 'grupa' unique
    id_Facultate = Column(Integer, ForeignKey('Facultate.id_Facultate'), nullable=False)
    facultate = relationship('Facultate')

# Profesor Table
class Profesor(Base):
    __tablename__ = 'Profesor'
    id_Profesor = Column(Integer, primary_key=True, autoincrement=True)
    nume = Column(VARCHAR(50), nullable=False)
    prenume = Column(VARCHAR(50), nullable=False)
    grad = Column(VARCHAR(50))
    id_Facultate = Column(Integer, ForeignKey('Facultate.id_Facultate'), nullable=False)
    facultate = relationship('Facultate')

# Materie Table
class Materie(Base):
    __tablename__ = 'Materie'
    id_Materie = Column(Integer, primary_key=True, autoincrement=True)
    nume = Column(VARCHAR(50), nullable=False)
    id_Profesor = Column(Integer, ForeignKey('Profesor.id_Profesor'), nullable=False)
    tip_examen = Column(VARCHAR(50))
    an_studiu = Column(Integer, nullable=False)
    semestru = Column(Integer, nullable=False)
    profesor = relationship('Profesor')

# Grupa_Examen Table (Link Table)
class GrupaExamen(Base):
    __tablename__ = 'Grupa_Examen'
    grupa = Column(VARCHAR(10), ForeignKey('Student.grupa'), primary_key=True, nullable=False)
    id_Examen = Column(Integer, ForeignKey('Examen.id_Examen'), primary_key=True, nullable=False)

# Cerere Table
class Cerere(Base):
    __tablename__ = 'Cerere'
    id_Cerere = Column(Integer, primary_key=True, autoincrement=True)
    id_Facultate = Column(Integer, ForeignKey('Facultate.id_Facultate'), nullable=False)
    id_Materie = Column(Integer, ForeignKey('Materie.id_Materie'), nullable=False)
    id_Profesor = Column(Integer, ForeignKey('Profesor.id_Profesor'), nullable=False)
    data = Column(Date, nullable=False)
    status = Column(VARCHAR(20), nullable=False)
    facultate = relationship('Facultate')
    materie = relationship('Materie')
    profesor = relationship('Profesor')

# Examen Table
class Examen(Base):
    __tablename__ = 'Examen'
    id_Examen = Column(Integer, primary_key=True, autoincrement=True)
    ora = Column(Time, nullable=False)
    sala = Column(VARCHAR(20), nullable=False)
    id_Profesor = Column(Integer, ForeignKey('Profesor.id_Profesor'))  # Foreign Key to Profesor for Assistant
    id_Cerere = Column(Integer, ForeignKey('Cerere.id_Cerere'), nullable=False)
    profesor = relationship('Profesor')
    cerere = relationship('Cerere')

# Facultate_Profesor Table (Link Table)
class FacultateProfesor(Base):
    __tablename__ = 'Facultate_Profesor'
    id_Facultate = Column(Integer, ForeignKey('Facultate.id_Facultate'), primary_key=True, nullable=False)
    id_Profesor = Column(Integer, ForeignKey('Profesor.id_Profesor'), primary_key=True, nullable=False)

# Asistent_Examen Table (Link Table)
class AsistentExamen(Base):
    __tablename__ = 'Asistent_Examen'
    id_Profesor = Column(Integer, ForeignKey('Profesor.id_Profesor'), primary_key=True, nullable=False)
    id_Examen = Column(Integer, ForeignKey('Examen.id_Examen'), primary_key=True, nullable=False)
