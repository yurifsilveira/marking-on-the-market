from sqlmodel import create_engine, SQLModel, Session
from fastapi import Depends, FastAPI
from typing import Annotated
from fastapi import APIRouter
from os import environ
from dotenv import load_dotenv
load_dotenv()

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
sqlite_url = environ['url_bank']

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session