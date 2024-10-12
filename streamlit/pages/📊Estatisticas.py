import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
from streamlit_echarts import st_echarts

import random
from pyecharts.charts import Bar
from pyecharts import options as opts
from streamlit_echarts import st_pyecharts
import numpy as np

# https://echarts.streamlit.app/
# Adicionando título 
# https://emojipedia.org/search?q=spy
st.title('Estatísticas 📊️')

# Função para renderizar o gráfico selecionado
def render_chart(chart_option):
    st_echarts(options=chart_option, height="400px")

# Define as opções para os dois gráficos

option2 = {
    "xAxis": {
        "type": "category",
        "data": ["A", "B", "C", "D", "E"],
    },
    "yAxis": {"type": "value"},
    "series": [{"data": [10, 20, 30, 40, 50], "type": "bar"}],
}

# Widget de seleção para escolher entre os gráficos
chart_selection = st.radio("Selecione o gráfico:", ("Patentes concedidas (16.1)", "Tempo de concessão de PI", "Tempo de concessão de PI (zoom)", "Gráfico 4", "Pedidos sub judice por Divisão Técnica (15.23)","Gráfico 5"))

# Renderiza o gráfico selecionado com base na seleção do usuário

if chart_selection == "Patentes concedidas (16.1)":
    
    texto = "Estatísticas de Patentes concedidas 16.1"
    # st.write(texto)
    st.markdown(f"""<div style="text-align: center; font-weight: bold; font-size: 14px;">{texto}</div>""", unsafe_allow_html=True)
    
    # SELECT year(data),count(*) FROM `arquivados` WHERE despacho='16.1' and year(data)>=2000 group by year(data) order by year(data) asc
    url = "http://www.cientistaspatentes.com.br/apiphp/patents/query/?q={%22mysql_query%22:%22year(data) as ano,count(*) FROM arquivados where despacho='16.1' and year(data)>=2000 group by year(data) order by year(data) asc%22}"

    # Definindo cabeçalhos para a requisição
    headers = {
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }


    try:
        # Requisição para obter os dados JSON
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Verificar se a requisição foi bem-sucedida

        # Tentar decodificar o JSON
        data = response.json()

        # Carregar os dados JSON em um DataFrame
        df = pd.DataFrame(data['patents'])
        df['ano'] = df['ano'].fillna('Unknown')

        # Verificar e converter a coluna 'count' para inteiro
        df['count'] = pd.to_numeric(df['count'], errors='coerce')

        # Mostrar o DataFrame
        # st.write("Valores", df)

        anos = df['ano'].tolist()
        counts = df['count'].tolist()

        option1 = {
            "xAxis": {
                "type": "category",
                "data": anos,
            },
            "yAxis": {"type": "value"},
            "series": [{"data": counts, "type": "bar"}],
        }
        
        render_chart(option1)

    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        st.error(f"Error occurred during request: {req_err}")
    except ValueError as json_err:
        st.error(f"JSON decode error: {json_err}")
    except Exception as err:
        st.error(f"An unexpected error occurred: {err}")
        
elif chart_selection == "Tempo de concessão de PI":
    texto = "Tempo de concessão de PI em anos x 100"
    # st.write(texto)
    st.markdown(f"""<div style="text-align: center; font-weight: bold; font-size: 14px;">{texto}</div>""", unsafe_allow_html=True)
    
    # SELECT data,round(100*tempo_concessoes) as tempo FROM estoque WHERE ano>=2010 and data<='2024-05-01' order by data asc;
    url = "http://www.cientistaspatentes.com.br/apiphp/patents/query/?q={%22mysql_query%22:%22data,round(100*tempo_concessoes) as tempo FROM estoque WHERE ano>=2010 and data<='2024-05-01' order by data asc%22}"

    # Definindo cabeçalhos para a requisição
    headers = {
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }


    try:
        # Requisição para obter os dados JSON
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Verificar se a requisição foi bem-sucedida

        # Tentar decodificar o JSON
        data = response.json()

        # Carregar os dados JSON em um DataFrame
        df = pd.DataFrame(data['patents'])
        df['data'] = df['data'].fillna('Unknown')

        # Verificar e converter a coluna 'count' para inteiro
        df['tempo'] = pd.to_numeric(df['tempo'], errors='coerce')

        # Mostrar o DataFrame
        # st.write("Valores", df)

        data = df['data'].tolist()
        tempo = df['tempo'].tolist()

        option2 = {
            "xAxis": {
                "type": "category",
                "data": data,
            },
            "yAxis": {"type": "value"},
            "series": [{"data": tempo, "type": "line"}],
        }
        
        render_chart(option2)

    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        st.error(f"Error occurred during request: {req_err}")
    except ValueError as json_err:
        st.error(f"JSON decode error: {json_err}")
    except Exception as err:
        st.error(f"An unexpected error occurred: {err}")

elif chart_selection == "Tempo de concessão de PI (zoom)":
    texto = "Tempo de concessão de PI em anos x 100"
    # st.write(texto)
    st.markdown(f"""<div style="text-align: center; font-weight: bold; font-size: 14px;">{texto}</div>""", unsafe_allow_html=True)
    
    # SELECT data,round(100*tempo_concessoes) as tempo FROM estoque WHERE ano>=2010 and data<='2024-05-01' order by data asc;
    url = "http://www.cientistaspatentes.com.br/apiphp/patents/query/?q={%22mysql_query%22:%22data,round(100*tempo_concessoes) as tempo FROM estoque WHERE ano>=2010 and data<='2024-05-01' order by data asc%22}"

    # Definindo cabeçalhos para a requisição
    headers = {
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }


    try:
        # Requisição para obter os dados JSON
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Verificar se a requisição foi bem-sucedida

        # Tentar decodificar o JSON
        data = response.json()

        # Carregar os dados JSON em um DataFrame
        df = pd.DataFrame(data['patents'])
        df['data'] = df['data'].fillna('Unknown')

        # Verificar e converter a coluna 'count' para inteiro
        df['tempo'] = pd.to_numeric(df['tempo'], errors='coerce')

        # Mostrar o DataFrame
        # st.write("Valores", df)

        data = df['data'].tolist()
        tempo = df['tempo'].tolist()

        b = (
            Bar()
            .add_xaxis(data)
            .add_yaxis("Tempo concessão de PI", tempo)
            .set_global_opts(
                title_opts=opts.TitleOpts(
                    title="Tempo de concessão de PI", subtitle="anos x 100"
                ),
                toolbox_opts=opts.ToolboxOpts(),
                tooltip_opts=opts.TooltipOpts(
                    trigger="axis", 
                    formatter="{a} <br/>{b}: {c} anos"
                ),
                xaxis_opts=opts.AxisOpts(
                    name="Data",
                    axislabel_opts=opts.LabelOpts(formatter="{value}")
                ),
                yaxis_opts=opts.AxisOpts(
                    name="",
                    axislabel_opts=opts.LabelOpts(formatter="{value} anos")
                )
            )
        )
        st_pyecharts(
            b, key="echarts"
        )  

    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        st.error(f"Error occurred during request: {req_err}")
    except ValueError as json_err:
        st.error(f"JSON decode error: {json_err}")
    except Exception as err:
        st.error(f"An unexpected error occurred: {err}")

elif chart_selection == "Gráfico 4":
    options = {
        "title": {"text": "Coordenações"},
        "tooltip": {"trigger": "axis"},
        "legend": {"data": ["CGPAT I", "CGPAT II", "CGPAT III", "CGPAT IV", "DIRPA"]},
        "grid": {"left": "3%", "right": "4%", "bottom": "3%", "containLabel": True},
        "toolbox": {"feature": {"saveAsImage": {}}},
        "xAxis": {
            "type": "category",
            "boundaryGap": False,
            "data": ["2015", "2016", "2017", "2018", "2019", "2020", "2021"],
        },
        "yAxis": {"type": "value"},
        "series": [
            {
                "name": "CGPAT I",
                "type": "line",
                "stack": "st",
                "data": [120, 132, 101, 134, 90, 230, 210],
            },
            {
                "name": "CGPAT II",
                "type": "line",
                "stack": "st",
                "data": [220, 182, 191, 234, 290, 330, 310],
            },
            {
                "name": "CGPAT III",
                "type": "line",
                "stack": "st",
                "data": [150, 232, 201, 154, 190, 330, 410],
            },
            {
                "name": "CGPAT IV",
                "type": "line",
                "stack": "st",
                "data": [320, 332, 301, 334, 390, 330, 320],
            },
            {
                "name": "DIRPA",
                "type": "line",
                "stack": "st",
                "data": [820, 932, 901, 934, 1290, 1330, 1320],
            },
        ],
    }
    st_echarts(options=options, height="400px")

elif chart_selection == "Gráfico 5":
        fig, ax = plt.subplots()
        df = pd.DataFrame()
        df['ano'] = [2020, 2021, 2022, 2023, 2024]
        df['prj'] = [2033.9, 2030.5, 2031.5, 2030.5, 2029.8]
        
        ax.plot(df['ano'], df['prj'], marker='o')

        # Adicionar linhas verticais
        anos_extendidos = np.arange(2020, 2031)
        for label in anos_extendidos:
            ax.axvline(x=label, color='gray', linestyle='--', linewidth=0.5)

        # Adicionar linhas horizontais
        for count in df['prj']:
            ax.axhline(y=count, color='gray', linestyle='--', linewidth=0.5)
 
        # Desenhar a reta de mínimos quadrados
        coef = np.polyfit(df['ano'], df['prj'], 1)
        poly1d_fn = np.poly1d(coef)
        #ax.plot(df['ano'], poly1d_fn(df['ano']), color='red', linestyle='-', label='Reta de Mínimos Quadrados')
        ax.plot(anos_extendidos, poly1d_fn(anos_extendidos), color='red', linestyle='-', label='Reta de Mínimos Quadrados')

        # escreve em cada ponto o valor de y
        for i, (ano, prj) in enumerate(zip(df['ano'], df['prj'])):
            ax.annotate(f'{prj}', (ano, prj), textcoords="offset points", xytext=(0,5), ha='center', fontsize=8)

        # Encontrar o ponto em que y = x na reta de mínimos quadrados
        for ano in anos_extendidos:
            y_value = poly1d_fn(ano)
            if np.isclose(y_value, ano, atol=1):  # Checar se y é aproximadamente igual a x (ano)
                ax.plot(ano, y_value, 'bo', label='Projeção')
                break
                
        # Adicionar rótulos e título
        ax.set_xlabel('Ano')
        ax.set_ylabel('Projeção')
        ax.set_title('Projeção de primeiro exame')
        ax.set_xticks(anos_extendidos)
        ax.set_xticklabels(anos_extendidos, rotation=90)
        ax.legend()

        # Mostrar o gráfico no Streamlit
        st.pyplot(fig)
else:
    url = "http://www.cientistaspatentes.com.br/apiphp/patents/query/?q={%22mysql_query%22:%22divisao,count(*)%20FROM%20arquivados%20where%20despacho=%2715.23%27%20and%20year(data)%3E=2000%20group%20by%20divisao%20order%20by%20count(*)%20desc%22}"
    # Definindo cabeçalhos para a requisição
    # http://www.cientistaspatentes.com.br/apiphp/patents/query/?q={"mysql_query":"divisao,count(*) FROM arquivados where despacho='15.23' and year(data)>=2000  group by divisao order by count(*) desc"
    headers = {
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }


    try:
        # Requisição para obter os dados JSON
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Verificar se a requisição foi bem-sucedida

        # Tentar decodificar o JSON
        data = response.json()

        # Carregar os dados JSON em um DataFrame
        df = pd.DataFrame(data['patents'])
        df['divisao'] = df['divisao'].fillna('Unknown')

        # Verificar e converter a coluna 'count' para inteiro
        df['count'] = pd.to_numeric(df['count'], errors='coerce')

        # Mostrar o DataFrame
        ## st.write("Valores", df)

        # Exibir o gráfico de linhas
        # st.line_chart(df.set_index('divisao')['count'])
        
        fig, ax = plt.subplots()
        ax.plot(df['divisao'], df['count'], marker='o')

        # Adicionar linhas verticais
        for i, label in enumerate(df['divisao']):
            ax.axvline(x=i, color='gray', linestyle='--', linewidth=0.5)

        # Adicionar linhas horizontais
        for count in df['count']:
            ax.axhline(y=count, color='gray', linestyle='--', linewidth=0.5)
            
        # Adicionar rótulos e título
        ax.set_xlabel('Divisão')
        ax.set_ylabel('Count')
        ax.set_title('Pedidos sub judice por Divisão Técnica (15.23)')
        ax.set_xticks(range(len(df['divisao'])))
        ax.set_xticklabels(df['divisao'], rotation=90)

        # Mostrar o gráfico no Streamlit
        st.pyplot(fig)

    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        st.error(f"Error occurred during request: {req_err}")
    except ValueError as json_err:
        st.error(f"JSON decode error: {json_err}")
    except Exception as err:
        st.error(f"An unexpected error occurred: {err}")