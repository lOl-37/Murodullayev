from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

DATABASE_URL = "sqlite:///./darslar.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Dars(Base):
    __tablename__ = "darslar"

    id = Column(Integer, primary_key=True, index=True)
    nomi = Column(String, index=True)
    daraja = Column(String)
    tavsif = Column(Text)
    video_url = Column(String, nullable=True)

    izohlar = relationship("Izoh", back_populates="dars", cascade="all, delete-orphan")

# app.py dagi xatolikni oldini olish uchun alias
DarsModel = Dars

class Izoh(Base):
    __tablename__ = "izohlar"

    id = Column(Integer, primary_key=True, index=True)
    dars_id = Column(Integer, ForeignKey("darslar.id"))
    username = Column(String)
    matn = Column(Text)
    rasm = Column(String, nullable=True)

    dars = relationship("Dars", back_populates="izohlar")

IzohModel = Izoh

def init_db():
    Base.metadata.create_all(bind=engine)
