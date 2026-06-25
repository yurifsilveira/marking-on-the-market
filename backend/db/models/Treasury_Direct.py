from sqlmodel import SQLModel, Field
from datetime import date
from typing import Optional


class Tesouro_Direto(SQLModel, table=True):

    id: Optional[str] = Field(default=None, primary_key=True)

    tipo: Optional[str] = Field(default=None, index=True)
    data: Optional[date] = Field(default=None, index=True)

    taxa_compra_manha: float
    taxa_venda_manha: float
    pu_compra_manha: float
    pu_venda_manha: float
    pu_base_manha: float

    vencimento: Optional[date] = Field(default=None, index=True)