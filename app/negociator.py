"""
    Modulo com ferramenta de integração 

"""
from pydantic import BaseModel, Field
from requests import get, post
from pandas import to_datetime, DataFrame, DateOffset , date_range
from datetime import date
from typing import List
from os import environ
from logging import info

from .api.db.models.usuario import Transacao
from .mathematical_graph.fabric import rolling_wind_to_title_treasure

class UserTitles(BaseModel):

    deadline:date
    dt: date
    price: float
    qt: int
    type: str


class Title_Operator():

    def __init__(self,user_name:str=None,email:str=None):

        users = get(environ["url_usuario"]).json()
        for user in users:

            if user["nome"] == user_name :
                self.id = user["id_usuario"]
                break
            elif user["email"] == email:
                self.id = user['id_usuario']
                break
            else:
                self.id = ""
                self.check_register_user()

    def check_register_user(self) -> bool:
        if self.id:
            return True
        raise ValueError("Usuário não encontrado na lista de cadastro!")

    def register_buy(self, release:UserTitles):

        self.check_register_user()

        id_title = "ltn" + release.dt.strftime("%d%m%Y") + release.deadline.strftime("%d%m%Y")
        payload = {
            "id_usuario": self.id,
            "id_titulo": id_title,
            "valor": release.price,
            "qtd": release.qt,
            "tipo": "compra"            
        }
        header = {"Content-Type": "application/json"}
        response = post(environ["url_cadastrar_transacao"], json = payload, headers= header)

        return response
    
    def register_sales(self, release:UserTitles):

        self.check_register_user()

        id_title = "ltn" + release.dt.strftime("%d%m%Y") + release.deadline.strftime("%d%m%Y")
        payload = {
            "id_usuario": self.id,
            "id_titulo": id_title,
            "valor": release.price,
            "qtd": release.qt,
            "tipo": "venda"            
        }
        header = {"Content-Type": "application/json"}
        response = post(environ["url_cadastrar_transacao"], json = payload, headers= header)

        return response
