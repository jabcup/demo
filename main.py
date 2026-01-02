from contextlib import asynccontextmanager
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel, Field
from sqlalchemy import select
from db import Base, engine, Libros, SessionLocal


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)


class LibroCreate(BaseModel):
    nombre: str = Field(max_length=150)
    descripcion: Optional[str] = Field(max_length=255)
    puntaje: int = Field(default=0)
    leido: bool = Field(default=False)


@app.post("/nuevo")
def create_book(payload: LibroCreate):
    libro = Libros(
        nombre=payload.nombre,
        descripcion=payload.descripcion,
        puntaje=payload.puntaje,
        leido=payload.leido,
    )

    with SessionLocal() as session:
        session.add(libro)
        session.commit()

    return {"resultado": "exito"}


@app.get("/")
def list_books():
    with SessionLocal() as session:
        stmt = select(Libros)
        libros = session.scalars(stmt).all()

    return {"libros": libros}
