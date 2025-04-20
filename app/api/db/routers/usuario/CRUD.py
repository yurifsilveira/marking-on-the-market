from fastapi import APIRouter, Query, HTTPException
from typing import Annotated, Optional
from datetime import date, datetime
from sqlmodel import select
from uuid import UUID
from ...models.usuario import Usuario
from ..config import SessionDep, get_session


router = APIRouter(
    prefix="/usuario",
    tags=["usuario"],
    responses={404: {"description": "Not found"}},
)

@router.post("/create/usuario/", response_model=Usuario)
def create(row: Usuario, session: SessionDep):
    session.add(row)
    session.commit()
    session.refresh(row)
    return row

@router.get("/read/usuario/")
def read_all(session: SessionDep) -> list[Usuario]:
    query = select(Usuario)
    rows = session.exec(query).all()
    return rows

@router.get("/read/usuario/{user}")
def read(
    session: SessionDep,
    user: str
) -> list[Usuario]:
    query = select(Usuario)
    if user:
        query = query.where(Usuario.nome == user)
    rows = session.exec(query).all()
    return rows

@router.delete("/delete/{user_id}")
def delete(user_id: str, session: SessionDep):
    user = session.get(Usuario, UUID(user_id))
    if not user:
        raise HTTPException(status_code=404, detail="Usuario not found")
    session.delete(user)
    session.commit()
    return {"ok": True}