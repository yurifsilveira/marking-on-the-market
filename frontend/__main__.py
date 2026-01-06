from flask import Flask, render_template, request
from flask_cors import CORS
from requests import get
from os import environ
from datetime import date
from pandas import to_datetime, DateOffset, DataFrame

environ["URL_LTN"] = "http://localhost:8000/investimento/renda_fixa/titulopublico"

app = Flask(__name__)

CORS(app)

@app.route("/rendafixa/<title>/<deadline>")
def render_title(title, deadline):

    data = get(environ["URL_LTN"] + f"?limit=100000000000&tipo={title}&deadline={deadline}").json()

    return data

@app.route("/rendafixa/<title>/")
def render_ltn(title):

    data = get(environ["URL_LTN"] + f"?limit=100000000000&title={title}").json()

    return data

@app.route("/rendafixa/detalhes")
def details():

    title = request.args.get("title")
    deadline = request.args.get("deadline")

    return render_template(
        "details.html",
        title=title,
        deadline=deadline
    )

@app.route("/cards")
def cards():
    
    days_of_wind  = 18
    dt = to_datetime(date.today()) - DateOffset(days=130)
    df = DataFrame(get(environ["URL_LTN"] + f"?limit=100000000000&start_date={dt.strftime("%Y-%m-%d")}").json())

    # Calculando a média movel 

    df = df.astype({"data":"datetime64[ns]"}).sort_values("data").reset_index(drop=True)
    for dt in df['vencimento'].drop_duplicates():
        filter_ = df.vencimento == dt
        _ = df.loc[filter_, ["pu_compra_manha","pu_venda_manha"]].rolling(days_of_wind).mean()

        df.loc[filter_, "pu_compra_manha_media_movel"] = _["pu_compra_manha"]
        df.loc[filter_, "pu_venda_manha_media_movel"] = _["pu_venda_manha"]

    df["data"] = df["data"].astype("datetime64[ns]").dt.strftime("%Y-%m-%d")
    df["vencimento"] = df["vencimento"].astype("datetime64[ns]").dt.strftime("%Y-%m-%d")

    df = df[df["data"] == df["data"].max()]
    df["titulo"] = df.vencimento.astype("datetime64[ns]").dt.strftime("%Y")

    title_public = df.to_dict("records")

    data = {"titulos_publicos": title_public}
    
    return data


@app.route("/rendafixa/home")
def render_public():

    return render_template("home.html")



app.run()