from enum import Enum

from datetime import date, datetime
from sqlmodel import Field, SQLModel, Integer
from pydantic import EmailStr
from uuid import UUID, uuid1

class Usuario(SQLModel,table=True):

    """
    Objeto de criação do usuário.
    
    Parameters
    -------------
        id_usuario (UUID): chave primaria do banco
        nome (str): Nome do usuário
    
    """
    id_usuario : UUID = Field(primary_key=True, default_factory= uuid1)
    nome : str

class Credential(SQLModel, table=True):

    """
    Objeto de criação das credenciais do usuário.
    
    Parameters
    -------------
        id_usuario (UUID): chave estrangeira do usuário
        senha (str): Senha do usuário
    
    """
    id_usuario : UUID = Field(foreign_key="usuario.id_usuario")
    senha : str

