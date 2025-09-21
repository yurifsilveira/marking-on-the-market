from enum import Enum

from datetime import date, datetime
from sqlmodel import Field, SQLModel, Integer
from pydantic import EmailStr, SecretStr
from uuid import UUID, uuid1

class Usuario(SQLModel,table=True):

    """
    Objeto de criação do usuário.
    
    Parameters
    -------------
        id_usuario (UUID): chave primaria do banco
        nome (str): Nome do usuário
        email (EmailStr): Email do usuário
    
    """
    id_usuario : UUID = Field(primary_key=True, default_factory= uuid1)
    nome : str
    email: EmailStr
    password: SecretStr

