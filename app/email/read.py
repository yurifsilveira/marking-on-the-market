"""
    Leitura dos e-mails com as transações dos usuários

"""
from tempfile import TemporaryDirectory
from pandas import read_excel
from os import environ
from requests import get

from ..negociator import UserTitles, Title_Operator
from  .gmail.read_email import Gmail

def _register_buys(buys, email, id_msg):
    operator = Title_Operator(email=email)
    for buy in buys:
        
        response = operator.register_buy(UserTitles(**buy))

        if response.ok:
        
            get(environ["url_cadastro_log_transacao"] + str(id_msg))

def _register_sales(sales, email, id_msg):
    operator = Title_Operator(email=email)
    for sale in sales:
        
        response = operator.register_sales(UserTitles(**sale))

        if response.ok:
        
            get(environ["url_cadastro_log_transacao"] + str(id_msg))

def register_transaction_by_user() -> None:
    """
        Esta função realizará o cadastro de todas as transações enviadas pelos usuários para e-mail.
        Ressalto que a informação é enviada via anexo ".xlsx", com uma planilha no seguinte modelo:
        | deadline | dt | price | qt | type | 
        O Assunto do e-mail é 'Transações Tesouro Selic'.
    """
    gmail = Gmail()
    gmail.mailbox.search("Transações Tesouro Selic")

    with TemporaryDirectory() as directory:

        logs_email = [ids.get("id") for ids in get(environ["url_cadastro_log_transacao"]).json()] #Verifica se já existe o cadastro dessa mensagem

        for msg in gmail.mailbox.messages:
            if msg.id in logs_email:continue
            for file in msg.files:

                filepath = file.attachment(directory)
                if not filepath:continue

                report_transaction = read_excel(filepath)

                init = msg.From.index("<")
                final = msg.From.index(">")
                email = msg.From[init+1:final]
                
                buys = report_transaction[report_transaction["type"]=="compra"].to_dict("records")
                sales = report_transaction[report_transaction["type"]=="venda"].to_dict("records")

                _register_buys(buys, email, msg.id)
                _register_sales(sales, email, msg.id)
                        
    return               
