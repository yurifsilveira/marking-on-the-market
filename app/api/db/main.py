from .routers import config, tesourodireto, transacao, usuario
from fastapi import FastAPI

app = FastAPI()
app.include_router(config.router)
app.include_router(tesourodireto.router)
app.include_router(transacao.router)
app.include_router(usuario.router)