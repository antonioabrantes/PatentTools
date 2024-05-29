import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
from streamlit_echarts import st_echarts

import random
from pyecharts.charts import Bar
from pyecharts import options as opts
from streamlit_echarts import st_pyecharts


# https://echarts.streamlit.app/
# Adicionando título 
# https://emojipedia.org/search?q=spy
st.title('Estatísticas 📊️')

# Adicionando descrição do projeto
st.write("Estatísticas de pedidos subjudice 15.23.")

# Função para renderizar o gráfico selecionado
def render_chart(chart_option):
    st_echarts(options=chart_option, height="400px")

# Define as opções para os dois gráficos
option1 = {
    "xAxis": {
        "type": "category",
        "data": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
    },
    "yAxis": {"type": "value"},
    "series": [{"data": [820, 932, 901, 934, 1290, 1330, 1320], "type": "line"}],
}

option2 = {
    "xAxis": {
        "type": "category",
        "data": ["A", "B", "C", "D", "E"],
    },
    "yAxis": {"type": "value"},
    "series": [{"data": [10, 20, 30, 40, 50], "type": "bar"}],
}

# Widget de seleção para escolher entre os gráficos
chart_selection = st.radio("Selecione o gráfico:", ("Gráfico 1", "Gráfico 2", "Gráfico 3", "Gráfico 4", "Gráfico 5"))

# Renderiza o gráfico selecionado com base na seleção do usuário
#if chart_selection == "Gráfico 1":
#    render_chart(option1)

if chart_selection == "Gráfico 1":
    my_sql = "divisao, count(*) FROM arquivados where despacho='15.23' and year(data)>=2000 group by divisao order by count(*) desc"
    url = "http://www.cientistaspatentes.com.br/apiphp/patents/query/?q={mysql_query:" + '"' + my_sql + '}"'

    url = "http://www.cientistaspatentes.com.br/apiphp/patents/query/?q={mysql_query:divisao,count(*) FROM%20arquivados%20where%20despacho=%2715.23%27%20and%20year(data)%3E=2000%20group%20by%20divisao%20order%20by%20count(*)%20desc%22}"

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
        df['divisao'] = df['divisao'].fillna('Unknown')

        # Verificar e converter a coluna 'count' para inteiro
        df['count'] = pd.to_numeric(df['count'], errors='coerce')

        # Mostrar o DataFrame
        st.write("Valores", df)

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
        ax.set_title('Incidência por Divisão Técnica')
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
        
elif chart_selection == "Gráfico 2":
    render_chart(option2)
elif chart_selection == "Gráfico 3":
    b = (
        Bar()
        .add_xaxis(["Microsoft", "Amazon", "IBM", "Oracle", "Google", "Alibaba"])
        .add_yaxis("2017-2018 Revenue in (billion $)", random.sample(range(100), 10))
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="Top cloud providers 2018", subtitle="2017-2018 Revenue"
            ),
            toolbox_opts=opts.ToolboxOpts(),
        )
    )
    st_pyecharts(
        b, key="echarts"
    )  # Add key argument to not remount component at every Streamlit run
    st.button("Randomize data")
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
else:
    url = "http://www.cientistaspatentes.com.br/apiphp/patents/query/?q={%22mysql_query%22:%22divisao,count(*)%20FROM%20arquivados%20where%20despacho=%2715.23%27%20and%20year(data)%3E=2000%20group%20by%20divisao%20order%20by%20count(*)%20desc%22}"
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
        df['divisao'] = df['divisao'].fillna('Unknown')

        # Verificar e converter a coluna 'count' para inteiro
        df['count'] = pd.to_numeric(df['count'], errors='coerce')

        # Mostrar o DataFrame
        st.write("Valores", df)

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
        ax.set_title('Incidência por Divisão Técnica')
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