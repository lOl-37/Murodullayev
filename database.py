from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./darslar.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class DarsModel(Base):
    __tablename__ = "darslar"
    id = Column(Integer, primary_key=True, index=True)
    nomi = Column(String, index=True)
    daraja = Column(String)
    tavsif = Column(Text)
    video_url = Column(String, nullable=True)
    kodlar = Column(Text, nullable=True)

class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)

class IzohModel(Base):
    __tablename__ = "izohlar"
    id = Column(Integer, primary_key=True, index=True)
    dars_id = Column(Integer, ForeignKey("darslar.id"))
    username = Column(String)
    matn = Column(Text)
    rasm = Column(String, nullable=True)

class SavolModel(Base):
    __tablename__ = "savollar"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    matn = Column(Text)
