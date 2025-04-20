
"""
    ESTE PACOTE TEM COMO OBJETIVO GERAR TODOS OS GRÁFICOS EM 'SVG' DA MARCAÇÃO AO MERCADO.
    Gráficos:
        - Preço de compra Vs média movel
        - Preço de vendas Vs média movel

"""

from pandas import DateOffset
from typing import List
from pydantic import BaseModel, Field
from datetime import date
import matplotlib.pyplot as plt
from pandas import to_datetime, DataFrame, DateOffset , date_range
from numpy import around
from requests import get
from datetime import date
from os import makedirs, environ

plt.rc('ytick', labelsize=11) 
plt.rc('xtick', labelsize=11)
plt.rc('font', family='Arial')

COLOR_PRICE = '#002060'
COLOR_ROLLING = '#B00000'

colors = {"compra":'red','venda':'green'}

makedirs("temp/img/compra",exist_ok=True)
makedirs("temp/img/venda",exist_ok=True)

class UserTitles(BaseModel):

    deadline:date
    dt: date
    price: float
    qt: int
    type: str

def rolling_wind_to_title_treasure(days_of_wind:int) -> DataFrame:

    """
    Retorna as informação do tesouro com o calculo da média movel definida pelo paramêtro 'days_of_wind'.
    """

    #media movel
    df = DataFrame(get(environ['url_bank_ltn_read']).json())
    df = df.astype({"data":"datetime64[ns]"}).sort_values("data").reset_index(drop=True)
    for dt in df['vencimento'].drop_duplicates():
        filter_ = df.vencimento == dt
        _ = df.loc[filter_, ["pu_compra_manha","pu_venda_manha"]].rolling(days_of_wind).mean()

        df.loc[filter_, "pu_compra_manha_media_movel"] = _["pu_compra_manha"]
        df.loc[filter_, "pu_venda_manha_media_movel"] = _["pu_venda_manha"]

    return df


def graph_sales_vs_rolling_wind(user_titles:List[UserTitles]=[],days_of_wind:int=18, path_file:'str'= "./temp/img/venda/"):

    """
    Gera um arquivo '.svg' de um gráfico do preço de venda vs média móvel de 18 dias, pode ser modificado definindo o valor
    do parametro 'days_of_wind'.

    """
    df = rolling_wind_to_title_treasure(days_of_wind)
    deadlines = set(df.vencimento.to_list())
    for dt in deadlines:
        df_view_rolling = df[(df.vencimento == dt ) & (df["data"] >= date.today() - DateOffset(days = 100) )]
        #Gráfico Comparando Preço de Venda

        #Index que mostraram os valores plotados
        index_with_min_values = df_view_rolling["pu_venda_manha"] == df_view_rolling[["pu_venda_manha"]].min().values[0]
        date_min_sales = to_datetime(df_view_rolling[index_with_min_values].data.values[0])
        value_min_sales = df_view_rolling[index_with_min_values]['pu_venda_manha'].values[0]
        index_with_max_values = df_view_rolling["pu_venda_manha"] == df_view_rolling[["pu_venda_manha"]].max().values[0]
        date_max_sales = to_datetime(df_view_rolling[index_with_max_values].data.values[0])
        value_max_sales = df_view_rolling[index_with_max_values]['pu_venda_manha'].values[0]

        #Valores Do Gráfico
        dates = df_view_rolling["data"].to_list()
        pu_sales = df_view_rolling["pu_venda_manha"].to_list()
        median_move_sales = df_view_rolling["pu_venda_manha_media_movel"].to_list()

        #Construindo O Gráfico
        fig, ax = plt.subplots(figsize=(13,7))
        fig.set_facecolor("white")

        fig.suptitle(f"LTN {to_datetime(dt).year} - Preço de Venda",fontsize=15, fontweight='bold', family= 'Arial',color=COLOR_PRICE ) 
        ax.plot(dates, pu_sales,COLOR_PRICE , linewidth = 1)
        ax.plot(dates, median_move_sales, ':',linewidth=1,color = COLOR_ROLLING)
        ax.set_xticks([date_min_sales, date_max_sales, dates[-1]])
        
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['left'].set_visible(False)

        #adicionando titulos do usuário ao gráfico
        for tt in user_titles:

            if (to_datetime(dt) == to_datetime(tt.deadline)) and (to_datetime(tt.dt) in to_datetime(dates)):
                index = dates.index(to_datetime(tt.dt))
                ax.plot(to_datetime(tt.dt), pu_sales[index],'o', markersize=5, color=colors.get(tt.type, 'transparent'))

        #Plotando pontos identificadores das anatoções 
        ax.plot([date_min_sales, dates[-1]], [value_min_sales,pu_sales[-1]],'o', markersize=5, color=COLOR_PRICE)

        #Plotando pontos anatoções 
        ax.annotate(value_min_sales, xy=(date_min_sales, value_min_sales), xytext=(date_min_sales, value_min_sales - 4), family= 'Arial',color=COLOR_PRICE,fontsize=11 )
        ax.annotate(value_max_sales, xy=(date_max_sales, value_max_sales), xytext=(date_max_sales, value_max_sales + 4), family= 'Arial',color=COLOR_PRICE,fontsize=11 )
        ax.annotate(pu_sales[-1], xy=(to_datetime(dates[-1]) + DateOffset(days=2), pu_sales[-1]), xytext=(to_datetime(dates[-1]) + DateOffset(days=2), pu_sales[-1]),fontsize=11, fontweight='bold', family= 'Arial',color=COLOR_PRICE )
        ax.set_ylim((value_min_sales - 20,value_max_sales + 20))

        ax.legend(
        handles=[plt.Line2D([0], [0], color=COLOR_PRICE ), plt.Line2D([0], [0], color=COLOR_ROLLING),
                plt.Line2D([0], [0], color='red', marker='o'), plt.Line2D([0], [0], color='green', marker='o')],
        labels=['Preço Título', 'Media Movel', 'Compra-Titulo','Venda-Titulo'],
        loc='upper right'
        )


        fig.savefig(path_file + f"LTN {to_datetime(dt).year} - Preço de Venda.png", metadata={'Date': None, 'Creator': None})

def graph_buys_vs_rolling_wind(user_titles:List[UserTitles]=[],path_file:'str'= "./temp/img/compra/",days_of_wind:int=18):

    """
    Gera um arquivo '.svg' de um gráfico do preço de compra vs média móvel de 18 dias, pode ser modificado definindo o valor
    do parametro 'days_of_wind'.

    """

    df = rolling_wind_to_title_treasure(days_of_wind)
    deadlines = set(df.vencimento.to_list())
    
    for dt in deadlines:
        df_view_rolling = df[(df.vencimento == dt) & (df["data"] >= date.today() - DateOffset(days = 100) )]
        #Gráfico Comparando Preço de Venda

        #Index que mostraram os valores plotados
        index_with_min_values = df_view_rolling["pu_compra_manha"] == df_view_rolling[["pu_compra_manha"]].min().values[0]
        date_min_buy = to_datetime(df_view_rolling[index_with_min_values].data.values[0])
        value_min_buy = df_view_rolling[index_with_min_values]['pu_compra_manha'].values[0]
        index_with_max_values = df_view_rolling["pu_compra_manha"] == df_view_rolling[["pu_compra_manha"]].max().values[0]
        date_max_buy = to_datetime(df_view_rolling[index_with_max_values].data.values[0])
        value_max_buy = df_view_rolling[index_with_max_values]['pu_compra_manha'].values[0]

        #Valores Do Gráfico
        dates = df_view_rolling["data"].to_list()
        pu_buy = df_view_rolling["pu_compra_manha"].to_list()
        median_move_sales = df_view_rolling["pu_compra_manha_media_movel"].to_list()

        #Construindo O Gráfico
        fig, ax = plt.subplots(figsize=(13,7))
        fig.set_facecolor("white")

        fig.suptitle(f"LTN {to_datetime(dt).year} - Preço de Compra",fontsize=15, fontweight='bold', family= 'Arial',color=COLOR_PRICE )
        ax.plot(dates, pu_buy,COLOR_PRICE , linewidth = 1)
        ax.plot(dates, median_move_sales, ':',linewidth=1,color = COLOR_ROLLING)
        ax.set_xticks([date_min_buy, date_max_buy, to_datetime(dates[-1])])

        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['left'].set_visible(False)

        #adicionando titulos do usuário ao gráfico
        for tt in user_titles:
            
            if (to_datetime(dt) == to_datetime(tt.deadline)) and (to_datetime(tt.dt) in to_datetime(dates)):
                index = dates.index(to_datetime(tt.dt))
                ax.plot(to_datetime(tt.dt) , pu_buy[index],'o', markersize=5, color=colors.get(tt.type, 'transparent'))

        #Plotando pontos identificadores das anatoções
        ax.plot([date_min_buy,dates[-1]],[value_min_buy,pu_buy[-1]],'o', markersize=5, color=COLOR_PRICE)

        #Plotando pontos anatoções 
        ax.annotate(value_min_buy, xy=(date_min_buy, value_min_buy), xytext=(date_min_buy, value_min_buy - 4), family= 'Arial',color=COLOR_PRICE ,fontsize=11)
        ax.annotate(value_max_buy, xy=(date_max_buy, value_max_buy), xytext=(date_max_buy, value_max_buy + 4), family= 'Arial',color=COLOR_PRICE,fontsize=11)
        ax.annotate(pu_buy[-1], xy=(to_datetime(dates[-1]) + DateOffset(days=1), pu_buy[-1]), xytext=(to_datetime(dates[-1]) + DateOffset(days=1), pu_buy[-1]),fontsize=11, fontweight='bold', family= 'Arial',color=COLOR_PRICE )
        ax.set_ylim((value_min_buy - 20,value_max_buy + 20))
        ax.legend(
        handles=[plt.Line2D([0], [0], color=COLOR_PRICE ), plt.Line2D([0], [0], color=COLOR_ROLLING),
                plt.Line2D([0], [0], color='red', marker='o'), plt.Line2D([0], [0], color='green', marker='o')],
        labels=['Preço Título', 'Media Movel', 'Compra-Titulo','Venda-Titulo'],
        loc='upper right'
        )

        fig.savefig(path_file + f"LTN {to_datetime(dt).year} - Preço de Compra.png", metadata={'Date': None, 'Creator': None})
