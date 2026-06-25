from src.treasury_direct import LTN, NTN
from os import environ
from datetime import date
from pandas import date_range
from requests import post, get, put
from pandas import DataFrame,concat, to_datetime
from dotenv import load_dotenv
load_dotenv()


response = get(environ["URL_LEITURA_TITULOS"])
if "Title not found" in response.text:
    
    ltn = LTN()
    df_ltn = ltn.extract_all_data()
    df_ltn["tipo"] = "LTN"
    ntn = NTN()
    df_ntn = ntn.extract_all_data()
    df_ntn["tipo"] = "NTN"

    df = concat([df_ltn, df_ntn])
    df =df.astype({"taxa_compra_manha": "float64", "taxa_venda_manha":"float64","pu_venda_manha":"float64", "pu_compra_manha":"float64", "pu_base_manha":"float64"})
    df["taxa_compra_manha"] = df["taxa_compra_manha"].round(3)
    df["taxa_venda_manha"] = df["taxa_venda_manha"].round(3)
    df["pu_compra_manha"] = df["pu_compra_manha"].round(3)
    df["pu_venda_manha"] = df["pu_venda_manha"].round(3)
    df["pu_base_manha"] = df["pu_base_manha"].round(3)
    df["data"] = to_datetime(df["data"], errors="coerce").dt.date
    df["vencimento"] = to_datetime(df["vencimento"], errors="coerce").dt.date
    df["data"] = df["data"].astype(str)
    df["vencimento"] = df["vencimento"].astype(str)
    del df["dia"]
    
    response = post(environ["URL_CADASTRO_TITULOS"], json= df.to_dict("records"))

else:
    
    df_all = DataFrame(response.json())
    year = df_all.data.astype("datetime64[ns]").dt.year.max()

    year = [year] if year == date.today().year else date_range(start=str(year), end=date.today(), freq="YS").year.to_list()
    ltn = LTN()

    df_ltn = ltn.extract_all_data(year)
    df_ltn["tipo"] = "LTN"
    ntn = NTN()
    df_ntn = ntn.extract_all_data(year)
    df_ntn["tipo"] = "NTN"
    
    df = concat([df_ltn, df_ntn])
    df =df.astype({"taxa_compra_manha": "float64", "taxa_venda_manha":"float64","pu_venda_manha":"float64" ,"pu_compra_manha":"float64", "pu_base_manha":"float64"})
    
    df["taxa_compra_manha"] = df["taxa_compra_manha"].round(3)
    df["taxa_venda_manha"] = df["taxa_venda_manha"].round(3)
    df["pu_compra_manha"] = df["pu_compra_manha"].round(3)
    df["pu_venda_manha"] = df["pu_venda_manha"].round(3)
    df["pu_base_manha"] = df["pu_base_manha"].round(3)
    df["data"] = to_datetime(df["data"], errors="coerce").dt.date
    df["vencimento"] = to_datetime(df["vencimento"], errors="coerce").dt.date
    df["data"] = df["data"].astype(str)
    df["vencimento"] = df["vencimento"].astype(str)
    del df["dia"]

    id_to_create = list(set(df.id.to_list()) - set(df_all.id.to_list()))
    id_to_update = list(set(df.id.to_list()) & set(df_all.id.to_list()))

    
    if id_to_create:
        
        response = post(environ["URL_CADASTRO_TITULOS"], json= df[df.id.isin(id_to_create)].to_dict("records"))

        
    if id_to_update:

        response = put(environ["URL_ATUALIZAR_TITULOS"], json= df[df.id.isin(id_to_update)].to_dict("records"))
    