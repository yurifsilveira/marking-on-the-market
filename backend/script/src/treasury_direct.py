from pandas import read_excel, DataFrame, concat, to_datetime, date_range
from datetime import date
from os import environ
from urllib.error import HTTPError
from typing import List

from src.logging_config import logger

pattern_date = r"[0-9]{2}[/][0-9]{2}[/][0-9]{0,4}"


class Treasury_Direct_Title:
    def __init__(self, url: str, days_of_wind: int):
        self.__url = url
        self.days_of_wind = days_of_wind
        logger.debug(f"Instanciado objeto Treasury_Direct_Title com URL base: {url}")

    def extract_data(self, year: int) -> DataFrame:
        try:
            logger.info(f"Iniciando extração do relatório {self.title}-{year}")
            response = read_excel(self.__url.format(year, year), sheet_name=None, header=None)
        except HTTPError as err:
            logger.error(f"Erro de conexão HTTP para {self.title}-{year}: {err}")
            err.add_note(f"Erro para URL: {self.__url.format(year, year)}")
            raise HTTPError(err)

        df = DataFrame()
        for key, value in response.items():
            try:
                deadline = value.loc[value[0] == "Vencimento", 1].to_list()[0]
                columns = value[value.index == 1].values
                value["Vencimento"] = deadline
                df = concat([df, value])
            except Exception as e:
                logger.warning(f"Falha ao processar aba '{key}' do relatório {self.title}-{year}: {e}")

        logger.debug("DataFrame concatenado com todas as abas processadas")

        df = df[df[0].str.contains(pattern_date, regex=True)]
        df.columns = columns.tolist()[0] + ["Vencimento"]
        df.columns = df.columns.str.replace(pattern_date, "", regex=True)
        df["Vencimento"] = to_datetime(df["Vencimento"], dayfirst=True)
        df["Data"] = to_datetime(df["Dia"], dayfirst=True)
        df = df[df["Vencimento"].dt.year > date.today().year + 1]
        df = df.sort_values("Data")
        
        df["id"] = (
            self.title
            + df["Data"].dt.strftime("%d%m%Y").astype("string")
            + df["Vencimento"].dt.strftime("%d%m%Y").astype("string")
        )
        df.reset_index(drop=True, inplace=True)
        df.columns = df.columns.str.lower().str.replace(" ", "_").str.replace("ã", "a")

        self.df = df
        logger.info(f"Relatório {self.title}-{year} concluído com {len(df)} registros")
        return df

    def extract_all_data(self, years: List[int] = None) -> DataFrame:
        if not years:
            years = date_range(end=date.today(), periods=20, freq="YE").year.to_list() + [date.today().year]
            logger.debug(f"Ano(s) padrão para extração definidos: {years}")

        logger.info(f"Iniciando extração de múltiplos anos para {self.title}: {years}")

        try:
            df = concat([self.extract_data(year) for year in years])
        except Exception as e:
            logger.error(f"Erro ao extrair dados de múltiplos anos ({self.title}): {e}")
            raise

        df = df.sort_values("data").reset_index(drop=True)
        df["data"] = to_datetime(df["data"], format="%Y-%m-%d").astype("str")
        df["vencimento"] = to_datetime(df["vencimento"], format="%Y-%m-%d").astype("str")

        logger.info(f"Extração consolidada para {self.title} concluída com {len(df)} registros totais")
        self.df = df
        return df


class LTN(Treasury_Direct_Title):
    title = "LTN"

    def __init__(self):
        self.url = environ["URL_TESOURO_DIRETO"] + "{}/LTN_{}.xls"
        super().__init__(self.url, 18)
        logger.debug(f"Classe {self.title} inicializada com URL base {self.url}")
        self.title = "LTN"


class NTN(Treasury_Direct_Title):
    title = "NTN"

    def __init__(self):
        self.url = environ["URL_TESOURO_DIRETO"] + "{}/NTN-B_Principal_{}.xls"
        super().__init__(self.url, 18)
        logger.debug(f"Classe {self.title} inicializada com URL base {self.url}")
        self.title="NTN"
