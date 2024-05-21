import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
from streamlit_echarts import st_echarts

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
chart_selection = st.radio("Selecione o gráfico:", ("Gráfico 1", "Gráfico 2", "Grafico3"))

# Renderiza o gráfico selecionado com base na seleção do usuário
if chart_selection == "Gráfico 1":
    render_chart(option1)
elif chart_selection == "Gráfico 2":
    render_chart(option2)
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