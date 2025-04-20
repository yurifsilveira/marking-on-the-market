from fastapi import APIRouter, Query, HTTPException
from typing import Annotated, Optional
from datetime import date, datetime
from sqlmodel import select
from uuid import UUID
from ...models.usuario import Usuario, Transacao
from ...models.email import email_log
from ..config import SessionDep, get_session

router = APIRouter(
    prefix="/transacao",
    tags=["transacao"],
    responses={404: {"description": "Not found"}},
)

@router.post("/create/transacao/", response_model=Transacao)
def create_usuario(row: Transacao, session: SessionDep):
    row.id_usuario = UUID(row.id_usuario)
    session.add(row)
    session.commit()
    session.refresh(row)
    return row

@router.get("/read/transacao/")
def read_ltn_all(session: SessionDep) -> list[Transacao]:
    query = select(Transacao)
    rows = session.exec(query).all()
    return rows

@router.get("/read/transacao/{user_id}")
def read_ltn_all(session: SessionDep, user_id: UUID) -> list[Transacao]:
    query = select(Transacao)
    if Transacao:
        query = query.where(Transacao.id_usuario == user_id)
    rows = session.exec(query).all()
    return rows


@router.get("/read/transacao/{id_transaction}")
def read_ltn(
    session: SessionDep,
    id_transaction: int
) -> list[Transacao]:
    query = select(Transacao)
    if Transacao:
        query = query.where(Transacao.id_transacao == id_transaction)
    rows = session.exec(query).all()
    return rows

@router.delete("/delete/{id_transaction}")
def delete_transaction(id_transaction: int, session: SessionDep):
    transaction = session.get(Usuario, id_transaction)
    if not transaction:
        raise HTTPException(status_code=404, detail="Usuario not found")
    session.delete(transaction)
    session.commit()
    return {"ok": True}

@router.get("/registre/log/email/{id_email}")
def create_log_email(id_email:str, session: SessionDep):
    id_email = email_log(id=id_email)
    session.add(id_email)
    session.commit()
    session.refresh(id_email)
    return {"ok":True}

@router.get("/registre/log/email/")
def read_log_email(session: SessionDep):
    query = select(email_log)
    rows = session.exec(query).all()
    return rows