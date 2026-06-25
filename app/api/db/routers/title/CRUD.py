from fastapi import APIRouter, Query, HTTPException, Depends
from typing import Annotated, Optional
from datetime import date, datetime
from sqlmodel import select
from ...models.tesouro import Titulo_LTN
from ...dependecies import SessionDep

router = APIRouter(
    prefix="/titulo",
    tags=["LTN"],
    responses={404: {"description": "Not found"}},
)

@router.post("/ltn", response_model=Titulo_LTN, status_code=201)
def create(row: Titulo_LTN, session: SessionDep) -> Titulo_LTN:

    row.data = datetime.strptime(row.data, "%Y-%m-%d").date() if isinstance(row.data, str) else row.data
    row.vencimento = datetime.strptime(row.vencimento, "%Y-%m-%d").date() if isinstance(row.vencimento, str) else row.vencimento

    session.add(row)
    session.commit()
    session.refresh(row)
    
    return row

@router.get("/ltn", status_code=200, response_model=list[Titulo_LTN])
def read(
        session: SessionDep,
        deadline: date = None      
         ) -> list[Titulo_LTN]:
    
    query = select(Titulo_LTN)
    query = query.where(Titulo_LTN.vencimento == deadline) if deadline else query
    rows = session.exec(query).all()

    if not rows:
        raise HTTPException(status_code=404, detail="LTN not found")
    
    return rows

@router.patch("/ltn", response_model=Titulo_LTN)
def update(ltn_id: str, 
           title_ltn: Titulo_LTN, 
           session: SessionDep):
    
    query = session.get(Titulo_LTN, ltn_id)

    title_ltn.data = datetime.strptime(title_ltn.data, "%Y-%m-%d").date() if isinstance(title_ltn.data, str) else title_ltn.data
    title_ltn.vencimento = datetime.strptime(title_ltn.vencimento, "%Y-%m-%d").date() if isinstance(title_ltn.vencimento, str) else title_ltn.vencimento

    if not query:
        raise HTTPException(status_code=404, detail="LTN not found")
    
    title_data = title_ltn.model_dump(exclude_unset=True)
    query.sqlmodel_update(title_data)
    session.add(query)
    session.commit()
    session.refresh(query)
    return query

@router.delete("/ltn", response_model=dict, status_code=200)
def delete(ltn_id: int, session: SessionDep):

    query = session.get(Titulo_LTN, ltn_id)
    if not query:
        raise HTTPException(status_code=404, detail="LTN not found")
    session.delete(query)
    session.commit()
    return {"ok": True}