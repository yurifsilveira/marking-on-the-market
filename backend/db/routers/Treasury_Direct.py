from fastapi import APIRouter,Depends, HTTPException
from typing import List
from sqlmodel import select, SQLModel
from datetime import date, datetime

from models import Treasury_Direct
from dependencies import get_session
from core import engine

router = APIRouter(
    prefix="/investimento/renda_fixa",
    tags= ["Tesouro Direto"],
)

@router.on_event("startup")
def on_startup(): 
    SQLModel.metadata.create_all(engine)


@router.get("/titulopublico", response_model= List[Treasury_Direct.Tesouro_Direto])
def read_title(start_date:date=None, 
               end_date:date=None,
               tipo:str=None,
               deadline:str=None, 
               limit=10,session = Depends(get_session)):
    """
    Retorna títulos do Tesouro Direto com filtros opcionais.

    Parameters
    -----------

    start_date: date
        Data inicial para filtrar os títulos (data >= start_date).
    end_date: date
        Data final para filtrar os títulos (data <= end_date).
    tipo: str
        Tipo do título (e.g., "LTN", "NTN-B", etc.).
    deadline: str
        Vencimento específico do título.
    limit: int
        Número máximo de títulos a serem retornados.
    session: Session
        Sessão do banco de dados injetada automaticamente.
    
    Returns
    --------
    List[Tesouro_Direto]
        Lista de títulos que correspondem aos filtros fornecidos.

    """

    statement = select(Treasury_Direct.Tesouro_Direto)
    
    if tipo:
        statement = statement.where(Treasury_Direct.Tesouro_Direto.tipo == tipo)
    if start_date:
        statement = statement.where(Treasury_Direct.Tesouro_Direto.data >= start_date)
    if end_date:
        statement = statement.where(Treasury_Direct.Tesouro_Direto.data <= end_date)
    if deadline:
        statement = statement.where(Treasury_Direct.Tesouro_Direto.vencimento == deadline)
    
    statement = statement.limit(limit)
    
    result = session.exec(statement).all()

    if not result:
        raise HTTPException(status_code=404, detail="Title not found")
    
    return result
    

@router.post("/titulopublico/create_em_massa", response_model=List[Treasury_Direct.Tesouro_Direto])
def create_titles(
    data: List[dict],  
    session= Depends(get_session)
):
    """
    Cria múltiplos títulos de uma vez, tratando tipos automaticamente.
    """
    try:

        register = []
        for item in data:

            for key in ["data", "vencimento"]:
                if isinstance(item[key], str):
                    try:

                        item[key] = datetime.strptime(item[key], "%Y-%m-%d").date()
                    except ValueError:
                        item[key] = datetime.strptime(item[key], "%d/%m/%Y").date()
                elif isinstance(item[key], datetime):
                    item[key] = item[key].date()

            for col in ["taxa_compra_manha", "taxa_venda_manha", "pu_compra_manha", "pu_venda_manha", "pu_base_manha"]:
                item[col] = float(item[col])

            register.append(Treasury_Direct.Tesouro_Direto(**item))
            
        session.add_all(register)
        session.commit()

        for r in register:
            session.refresh(r)

        return register

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao criar títulos: {str(e)}")


@router.put("/titulopublico/update_em_massa", response_model=List[Treasury_Direct.Tesouro_Direto])
def update_titles(
    data: List[Treasury_Direct.Tesouro_Direto],
    session=Depends(get_session)
):
    """
    Atualiza múltiplos títulos de uma vez (por id).
    """
    updated_items = []

    for item in data:
        # Converter o modelo para dict para manipulação mais fácil
        item_data = item.dict(exclude_unset=True)

        # 🔹 Normalizar datas
        for key in ["data", "vencimento"]:
            if key in item_data:
                value = item_data[key]
                if isinstance(value, str):
                    try:
                        item_data[key] = datetime.strptime(value, "%Y-%m-%d").date()
                    except ValueError:
                        item_data[key] = datetime.strptime(value, "%d/%m/%Y").date()
                elif isinstance(value, datetime):
                    item_data[key] = value.date()

        # 🔹 Converter valores numéricos
        for col in ["taxa_compra_manha", "taxa_venda_manha", "pu_compra_manha", "pu_venda_manha", "pu_base_manha"]:
            if col in item_data and item_data[col] is not None:
                item_data[col] = float(item_data[col])

        # 🔹 Buscar registro existente
        db_item = session.get(Treasury_Direct.Tesouro_Direto, item.id)
        if not db_item:
            raise HTTPException(status_code=404, detail=f"Título com id {item.id} não encontrado")

        # 🔹 Atualizar os campos
        for key, value in item_data.items():
            setattr(db_item, key, value)

        updated_items.append(db_item)

    try:
        session.commit()
        for i in updated_items:
            session.refresh(i)
        return updated_items
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao atualizar títulos: {str(e)}")
