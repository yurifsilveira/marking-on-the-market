from sqlmodel import SQLModel, Field
from datetime import date


class Tesouro_Direto(SQLModel, table=True):

    id: str | None = Field(default=None, primary_key=True)
    tipo: str = Field(default=None, index=True)
    data: date = Field(default=None, index=True)
    taxa_compra_manha:float
    taxa_venda_manha: float
    pu_compra_manha: float
    pu_venda_manha:float
    pu_base_manha:float
    vencimento:date = Field(default=None, index=True)
    