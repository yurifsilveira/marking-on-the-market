from fastapi import APIRouter, Query, HTTPException
from typing import Annotated, Optional
from datetime import date, datetime
from sqlmodel import select
from ..models.tesouro import LOGS
from ..config import SessionDep

router = APIRouter(
    prefix="/titulo-tesouro",
    tags=["logs"],
    responses={404: {"description": "Not found"}},
)

@router.post("/logs/", response_model=LOGS)
def create_log(row: LOGS, session: SessionDep):

    row.timestamp = datetime.strptime(row.timestamp, "%Y-%m-%d").date() if isinstance(row.timestamp, str) else row.timestamp
    session.add(row)
    session.commit()
    session.refresh(row)
    return row

@router.get("/logs/")
def read_logs(session: SessionDep) -> list[LOGS]:
    query = select(LOGS)
    rows = session.exec(query).all()
    return rows
