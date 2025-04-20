from fastapi import APIRouter, Query, HTTPException
from typing import Annotated, Optional
from datetime import date, datetime
from sqlmodel import select
from ...models.tesouro import TituloLTN
from ..config import SessionDep, get_session

router = APIRouter(
    prefix="/titulo-tesouro",
    tags=["titulo-tesouro"],
    responses={404: {"description": "Not found"}},
)

@router.post("/create/ltn/", response_model=TituloLTN)
def create(row: TituloLTN, session: SessionDep):
    row.data = datetime.strptime(row.data, "%Y-%m-%d").date() if isinstance(row.data, str) else row.data
    row.vencimento = datetime.strptime(row.vencimento, "%Y-%m-%d").date() if isinstance(row.vencimento, str) else row.vencimento

    session.add(row)
    session.commit()
    session.refresh(row)
    return row

@router.get("/read/ltn/")
def read_all(session: SessionDep) -> list[TituloLTN]:
    query = select(TituloLTN)
    rows = session.exec(query).all()
    return rows

@router.get("/read/ltn/{deadline}")
def read(
    session: SessionDep,
    deadline: date
) -> list[TituloLTN]:
    query = select(TituloLTN)
    if deadline:
        query = query.where(TituloLTN.vencimento == deadline)
    rows = session.exec(query).all()
    return rows

@router.patch("/update/ltn/")
def update(ltn_id: str, title_ltn: TituloLTN, session: SessionDep):
    ltn_db = session.get(TituloLTN, ltn_id)

    title_ltn.data = datetime.strptime(title_ltn.data, "%Y-%m-%d").date() if isinstance(title_ltn.data, str) else title_ltn.data
    title_ltn.vencimento = datetime.strptime(title_ltn.vencimento, "%Y-%m-%d").date() if isinstance(title_ltn.vencimento, str) else title_ltn.vencimento

    if not ltn_db:
        raise HTTPException(status_code=404, detail="LTN not found")
    title_data = title_ltn.model_dump(exclude_unset=True)
    ltn_db.sqlmodel_update(title_data)
    session.add(ltn_db)
    session.commit()
    session.refresh(ltn_db)
    return ltn_db

@router.delete("/delete/{ltn_id}")
def delete(ltn_id: int, session: SessionDep):
    ltn = session.get(TituloLTN, ltn_id)
    if not ltn:
        raise HTTPException(status_code=404, detail="LTN not found")
    session.delete(ltn)
    session.commit()
    return {"ok": True}