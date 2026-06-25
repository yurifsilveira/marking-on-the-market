from typing import Annotated

from datetime import date, datetime
from sqlmodel import Field, SQLModel, Integer
from uuid import UUID, uuid1
from enum import Enum

class Titulo_LTN(SQLModel,table=True):
    """
    Objeto de criação do título LTN.

    Parameters
    -------------
        id (str): chave primaria do banco
        data (date): Data correlacionada com o preço do titulo
        taxa_compra_manha (float): Taxa de Compra do Titulo
        taxa_venda_manha (float) : Taxa de Venda do Titulo
        pu_compra_manha (float) : Preço de Compra do Titulo
        pu_venda_manha (float) : Preço de Venda do Titulo
        pu_base_manha (float) : Preço Base de Venda
        vencimento (date) : Data de Vencimento do Titulo

    """

    id : str = Field(primary_key=True)
    data : date = Field(index=True, description="Data correlacionada com o preço do titulo")
    taxa_compra_manha :float = Field(description = "Taxa de Compra do Titulo")
    taxa_venda_manha : float = Field(description = "Taxa de Venda do Titulo")
    pu_compra_manha : float = Field(description = "Preço de Compra do Titulo")
    pu_venda_manha : float = Field(description = "Preço de Venda do Titulo")
    pu_base_manha: float = Field(description = "Preço Base de Venda")
    vencimento: date = Field(description = "Data de Vencimento do Titulo")

class TipoMovimento(str, Enum):
    """
    Enumeração para os tipos de movimento: compra ou venda.

    Parameters
    -------------
       compra (str): Representa uma operação de compra.
       venda (str): Representa uma operação de venda.

    """
    compra = "compra"
    venda = "venda"

class Transacao(SQLModel,table=True):
    """
    Objeto de criação da transação.
    
    Parameters
    -------------
        id_transacao (UUID): chave primaria do banco
        id_usuario (UUID): chave estrangeira do usuário
        id_titulo (str): chave estrangeira do título
        valor (float): Valor da transação
        qtd (int): Quantidade
    """

    id_transacao : UUID = Field(primary_key=True, default_factory= uuid1)
    id_usuario : UUID = Field(default= None, foreign_key = "usuario.id_usuario")
    id_titulo : str = Field(default= None, foreign_key = "tituloltn.id")
    valor : float = Field(default=None)
    qtd : int = Field(default=None)
    tipo :  TipoMovimento = Field(default=None)

