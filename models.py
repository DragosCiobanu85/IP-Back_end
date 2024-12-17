from sqlalchemy import Column, Integer, String, ForeignKey, Date, Time, CheckConstraint
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.dialects.mssql import VARCHAR

from database import Base

# Declaring Base
#Base = declarative_base()

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
    parola = Column(VARCHAR(450), nullable=False)
    rol = Column(VARCHAR(20), nullable=False)  # Role can be 'Student' or 'Profesor'

    __table_args__ = (
        CheckConstraint("rol IN ('Student', 'Profesor')", name="check_user_role"),
    )
    student = relationship('Student', back_populates='user', uselist=False)
    profesor = relationship('Profesor', back_populates='user', uselist=False)

class Grupa(Base):
    __tablename__ = 'Grupa'
    id_Grupa = Column(Integer, primary_key=True, autoincrement=True)
    nume = Column(VARCHAR(10), nullable=False, unique=True)
    id_Facultate = Column(Integer, ForeignKey('Facultate.id_Facultate'), nullable=False)
    facultate = relationship('Facultate')

# Student Table
class Student(Base):
    __tablename__ = 'Student'
    id_Student = Column(Integer, primary_key=True, autoincrement=True)
    nume = Column(VARCHAR(50), nullable=False)
    prenume = Column(VARCHAR(50), nullable=False)
    id_Grupa = Column(Integer, ForeignKey('Grupa.id_Grupa'), nullable=False)
    id_user = Column(Integer, ForeignKey('User.id_user'), nullable=False, unique=True)

    grupa = relationship('Grupa')
    user = relationship('User', back_populates='student')


# Profesor Table
class Profesor(Base):
    __tablename__ = 'Profesor'
    id_Profesor = Column(Integer, primary_key=True, autoincrement=True)
    nume = Column(VARCHAR(50), nullable=False)
    prenume = Column(VARCHAR(50), nullable=False)
    grad = Column(VARCHAR(50))
    id_Facultate = Column(Integer, ForeignKey('Facultate.id_Facultate'), nullable=False)
    id_user = Column(Integer, ForeignKey('User.id_user'), nullable=False, unique=True)

    facultate = relationship('Facultate')
    user = relationship('User', back_populates='profesor')

# Materie Table
class Materie(Base):
    __tablename__ = 'Materie'
    id_Materie = Column(Integer, primary_key=True, autoincrement=True)
    nume = Column(VARCHAR(50), nullable=False)
    id_Profesor = Column(Integer, ForeignKey('Profesor.id_Profesor'), nullable=False)
    tip_examen = Column(VARCHAR(50))
    an_studiu = Column(Integer)
    semestru = Column(Integer)
    profesor = relationship('Profesor')

# Grupa_Examen Table (Link Table)
class GrupaExamen(Base):
    __tablename__ = 'Grupa_Examen'
    grupa_id = Column(Integer, ForeignKey('Grupa.id_Grupa'), primary_key=True, nullable=False)
    id_Examen = Column(Integer, ForeignKey('Examen.id_Examen'), primary_key=True, nullable=False)
    examen = relationship('Examen')
    grupa = relationship('Grupa')


# Cerere Table
class Cerere(Base):
    __tablename__ = 'Cerere'
    id_Cerere = Column(Integer, primary_key=True, autoincrement=True)
    id_Facultate = Column(Integer, ForeignKey('Facultate.id_Facultate'), nullable=False)
    id_Materie = Column(Integer, ForeignKey('Materie.id_Materie'), nullable=False)
    id_Profesor = Column(Integer, ForeignKey('Profesor.id_Profesor'), nullable=False)
    id_Student = Column(Integer, ForeignKey('Student.id_Student'), nullable=False)
    id_Grupa = Column(Integer, ForeignKey('Grupa.id_Grupa'), nullable=False)
    data = Column(Date, nullable=False)
    status = Column(VARCHAR(20), nullable=False)
    grupa = relationship('Grupa')
    facultate = relationship('Facultate')
    materie = relationship('Materie')
    profesor = relationship('Profesor')
    student = relationship('Student')
    # Constrângerea pentru status
    __table_args__ = (
        CheckConstraint("status IN ('in asteptare', 'acceptata', 'respinsa')", name="check_cerere_status"),
    )

# Examen Table
class Examen(Base):
    __tablename__ = 'Examen'
    id_Examen = Column(Integer, primary_key=True, autoincrement=True)
    id_Facultate = Column(Integer, ForeignKey('Facultate.id_Facultate'), nullable=False)
    id_Profesor = Column(Integer, ForeignKey('Profesor.id_Profesor'),nullable=False)
    id_Profesor_1 = Column(Integer, ForeignKey('Profesor.id_Profesor'),nullable=False)  # Foreign Key to Profesor for Assistant
    id_Materie = Column(Integer, ForeignKey('Materie.id_Materie'), nullable=False)
    id_Grupa = Column(Integer, ForeignKey('Grupa.id_Grupa'), nullable=False)
    data = Column(Date, nullable=False)
    id_Sala = Column(Integer, ForeignKey('Sala.id_Sala'),nullable=False)
    ora = Column(Time, nullable=False)
    id_Cerere = Column(Integer, ForeignKey('Cerere.id_Cerere', ondelete='CASCADE'), nullable=True)
    grupa= relationship('Grupa')
    facultate=relationship('Facultate')
    materie=relationship('Materie')
    sala=relationship('Sala')
    profesor = relationship('Profesor', foreign_keys=[id_Profesor])  # Profesor principal
    asistent = relationship('Profesor', foreign_keys=[id_Profesor_1])
    cerere = relationship('Cerere')

# Facultate_Profesor Table (Link Table)
class FacultateProfesor(Base):
    __tablename__ = 'Facultate_Profesor'
    id_Facultate = Column(Integer, ForeignKey('Facultate.id_Facultate'), primary_key=True, nullable=False)
    id_Profesor = Column(Integer, ForeignKey('Profesor.id_Profesor'), primary_key=True, nullable=False)

# Asistent_Examen Table (Link Table)
class AsistentExamen(Base):
    __tablename__ = 'Asistent_Examen'
    id_Profesor_1 = Column(Integer, ForeignKey('Profesor.id_Profesor'), primary_key=True, nullable=False)
    id_Examen = Column(Integer, ForeignKey('Examen.id_Examen'), primary_key=True, nullable=False)

class Sala(Base):
    __tablename__ = 'Sala'
    id_Sala = Column(Integer, primary_key=True, autoincrement=True)
    nume = Column(VARCHAR(50), nullable=False)
