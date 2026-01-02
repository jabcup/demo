import os
from sqlalchemy import CheckConstraint, create_engine, String, Integer, Boolean, Column
from sqlalchemy.orm import sessionmaker, declarative_base

DB = os.getenv("DATABASE_URL")

if not DB:
    DB = "sqlite:///./demo.db"
elif DB.startswith("postgres://"):
    DB = DB.replace("postgres://", "postgresql://", 1)

engine = create_engine(DB, pool_pre_ping=True, echo=False)
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()


class Libros(Base):
    __tablename__ = "libros"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(150), nullable=False)
    descripcion = Column(String(255), nullable=True)
    puntaje = Column(Integer, nullable=True)
    leido = Column(Boolean, default=False)

    __table_args__ = (
        CheckConstraint("puntaje BETWEEN 0 AND 10", name="rango_puntaje"),
    )
