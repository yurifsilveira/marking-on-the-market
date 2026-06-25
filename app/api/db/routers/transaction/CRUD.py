from fastapi import APIRouter, Query, HTTPException
from typing import Annotated, Optional
from datetime import date, datetime
from sqlmodel import select
from uuid import UUID
from ...models.tesouro import Transacao
from ...dependecies import SessionDep

router = APIRouter(
    tags=["Transacao"],
    responses={404: {"description": "Not found"}},
)

@router.post("/transacao", response_model=Transacao, status_code=201)
def create_transaction(row: Transacao, session: SessionDep):
    row.id_usuario = UUID(row.id_usuario)
    session.add(row)
    session.commit()
    session.refresh(row)
    return row

@router.get("/transacao")
def read_transaction(session: SessionDep,
             user_id: UUID = None,
             limit: int = 1000,
             id_transaction: int = None
             ) -> list[Transacao]:
    
    query = select(Transacao)
    query = query.where(Transacao.id_usuario == user_id) if user_id else query
    query = query.where(Transacao.id_transacao == id_transaction) if id_transaction else query
    query = query.limit(limit) if limit else query
    rows = session.exec(query).all()

    if not rows:
        raise HTTPException(status_code=404, detail="Transacao not found")
    return rows

@router.delete("/transacao")
def delete_transaction(id_transaction: int, session: SessionDep):

    transaction = session.get(Transacao,id_transaction)
    if not transaction:
        raise HTTPException(status_code=404, detail="id_transaction not found")
    session.delete(transaction)
    session.commit()
    return {"ok": True}
