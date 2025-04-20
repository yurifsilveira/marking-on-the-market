from enum import Enum

from datetime import date, datetime
from sqlmodel import Field, SQLModel, Integer
from pydantic import EmailStr
from uuid import UUID, uuid1

class TipoMovimento(str, Enum):
    compra = "compra"
    venda = "venda"

class Usuario(SQLModel,table=True):

    id_usuario : UUID = Field(primary_key=True, default_factory= uuid1)
    nome : str
    email: EmailStr

class Transacao(SQLModel,table=True):

    id_transacao : UUID = Field(primary_key=True, default_factory= uuid1)
    id_usuario : UUID = Field(default= None, foreign_key = "usuario.id_usuario")
    id_titulo : str = Field(default= None, foreign_key = "tituloltn.id")
    valor : float = Field(default=None)
    qtd : int = Field(default=None)
    tipo :  TipoMovimento