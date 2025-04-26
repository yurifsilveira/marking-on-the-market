from pandas import read_csv, read_excel, DataFrame, concat, to_datetime, date_range
from datetime import date
from io import BytesIO, StringIO
from os import environ

# environ["URL_TESOURO_DIRETO"] = f"https://cdn.tesouro.gov.br/sistemas-internos/apex/producao/sistemas/sistd/"

pattern_date = '[0-9]{2}[/][0-9]{2}[/][0-9]{0,4}'

def extract_data(year):

    response = read_excel(environ["URL_TESOURO_DIRETO"]+ f"{year}/LTN_{year}.xls", sheet_name=None,header=None)
    df = DataFrame()
    value = ''
    for key,value in response.items():
        deadline = value.loc[value[0] == 'Vencimento', 1].to_list()[0]
        columns = value[value.index== 1].values 
        value['Vencimento'] = deadline
        df = concat([df, value])


    df = df[df[0].str.contains(pattern_date, regex=True)]
    df.columns = columns.tolist()[0] + ["Vencimento"]
    df.columns = df.columns.str.replace(pattern_date,"", regex=True)
    df['Vencimento'] = to_datetime(df['Vencimento'],dayfirst=True)
    df["Data"] = to_datetime(df['Dia'],dayfirst=True)
    return df