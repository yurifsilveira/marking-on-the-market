from datetime import date
from pandas import DataFrame, concat, date_range
from requests import post, get
from os import environ
from json import dumps

from dotenv import load_dotenv
load_dotenv()

from .scrapt import extract_data

def search_ltn_year() -> DataFrame:

    df = extract_data(date.today().year)
    df = df[df['Vencimento'].dt.year > date.today().year + 1]
    df = df.sort_values('Data')
    df['id'] = 'ltn' + df['Data'].dt.strftime("%d%m%Y").astype("string") + df['Vencimento'].dt.strftime('%d%m%Y').astype("string")
    df.reset_index(drop=True, inplace=True)
    df.columns = df.columns.str.lower()
    df.columns = df.columns.str.replace(' ','_').str.replace("ã",'a')

    return df

def start_db():
    
    df = concat([extract_data(date.today().year) for year in date_range(end=date.today(), periods=7, freq='Y').year + [date.today().year]])
    df = df[df['Vencimento'].dt.year > date.today().year + 1]
    df = df.sort_values('Data')
    df['id'] = 'ltn' + df['Data'].dt.strftime("%d%m%Y").astype("string") + df['Vencimento'].dt.strftime('%d%m%Y').astype("string")
    df.reset_index(drop=True, inplace=True)
    df.columns = df.columns.str.lower()
    df.columns = df.columns.str.replace(' ','_').str.replace("ã",'a')
    
    return df


