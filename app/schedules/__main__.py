from rocketry import Rocketry
from rocketry.conds import daily
from time import sleep
from datetime import date
from os import environ
from requests import post, get, patch
from json import dumps
from dotenv import load_dotenv
load_dotenv()
import logging
from logging.handlers import HTTPHandler


from src import script

app = Rocketry()

# handler = HTTPHandler(host='http:localhost:8000', url='/titulo-tesouro/logs/', method='POST', secure=False)
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# handler.setFormatter(formatter)
# logger = logging.getLogger('rocketry.task')

# logger.addHandler(handler)

ltns = get(environ["url_bank_ltn_read"]).json()

if not ltns:
    script.start_db()

@app.task(daily.at("15:35:00"))
def search_first_update_title():
    
    df = script.search_ltn_year()
    
    ltns = get(environ['url_bank_ltn_read']).json()
    ids = [ltn['id'] for ltn in ltns]
    df = df[~df.id.isin(ids)]

    for index in df.index:

        response = post(environ['url_bank_ltn'], dumps(df[df.index==index].astype("string").to_dict('records')[0]))
        id = df[df.index==index].astype("string").to_dict('records')[0]['id']
        if not response.ok:
            ...
        print(f"{id} criado no banco!")

@app.task(daily.at('13:00') | daily.on('15:44') )
def search_other_update_title():

    df = script.search_ltn_year()
    ltns = get(environ["url_bank_ltn_read"]).json()
    ids = [ltn['id'] for ltn in ltns]
    df = df[df.id.isin(ids)]
    df['id'] = 'ltn' + df['data'].dt.strftime("%d%m%Y").astype("string") + df['vencimento'].dt.strftime('%d%m%Y').astype("string")
    df = df.astype({
        "data":"string",
        "vencimento":"string"
    })

    for index in df.index:

        ltn_id = df[df.index==index].astype("string").to_dict('records')[0]['id']
        data = df[df.index==index].to_dict('records')[0]

        response = patch(environ['url_bank_ltn_update'], params={"ltn_id":ltn_id},json =data)

        if not response.ok:
            ...
        print(f"{ltn_id} atualizado no banco!")

search_first_update_title()
app.run()