from typing import Annotated

from datetime import date, datetime
from sqlmodel import Field, SQLModel, Integer

class TituloLTN(SQLModel,table=True):

    id : str = Field(primary_key=True)
    data : date = Field(index=True, description="Data correlacionada com o preço do titulo")
    taxa_compra_manha :float = Field(description = "Taxa de Compra do Titulo")
    taxa_venda_manha : float = Field(description = "Taxa de Venda do Titulo")
    pu_compra_manha : float = Field(description = "Preço de Compra do Titulo")
    pu_venda_manha : float = Field(description = "Preço de Venda do Titulo")
    pu_base_manha: float = Field(description = "Preço Base de Venda")
    vencimento: date = Field(description = "Data de Vencimento do Titulo")

class LOGS(SQLModel,table=True):

    id : int = Field(default=None,primary_key=True)
    timestamp : datetime
    level: str
    message : str
