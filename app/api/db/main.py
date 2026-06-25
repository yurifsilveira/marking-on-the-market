from . import config
from .routers import title, transaction
from fastapi import FastAPI


app = FastAPI(
    title="API Tesouro Direto BRL"
)

prefix="/v1/tesouro-direto/BRL"

config.create_db_and_tables()

app.include_router(title.router, prefix=prefix)
app.include_router(transaction.router, prefix=prefix)