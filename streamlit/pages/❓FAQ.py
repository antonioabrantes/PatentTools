import streamlit as st

from pathlib import Path
from dotenv import load_dotenv
import pandas as pd
import numpy as np
import os
import sys
import time
from jobs_details import jobs_details as data
from dotenv import load_dotenv
import ast

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

st.title('FAQ ❓')
st.write("Perguntas mais frequentes.")
#st.write(f"perguntas = {data}")

try:
    # Converte a string para uma lista de dicionários
    #data_list = ast.literal_eval(data)
    data_list = data

    # Função para imprimir os campos de forma formatada
    def print_data(data):
        for item in data:
            st.markdown(f"#Tema: {item['Tema']}")
            st.write(f"**Pergunta:** {item['Pergunta']}")
            st.write(f"**Resposta:** {item['Resposta']}")
            st.write(f"**Modelos:** {item['Modelos']}")
            st.write(f"**Despacho:** {item['Despacho']}")
            st.write("\n" + "="*20 + "\n")

    # Executa a função para imprimir os dados
    print_data(data_list)

except ValueError as e:
    st.error(f"Erro ao converter a string: {e}")