import streamlit as st

from pathlib import Path
import google.generativeai as genai
from dotenv import load_dotenv
import pandas as pd
import numpy as np
import os
import sys
import time
from jobs_details import jobs_details as data
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# arquivo JSON https://jsoneditoronline.org/

# Configura a API para o modelo genai
# Obtém a chave da API da variável de ambiente
# no streamlit https://share.streamlit.io/ escolha o app / Settings / Secrets e guarde a chave API do Google
api_key = os.getenv("GEMINI_API_KEY")
#st.write(api_key)
genai.configure(api_key=api_key)

# Instrução do sistema para o modelo generativo
system_instruction = f"""

Seu nome é Sophia, um assistente virtual que ajuda o examinador de patentes a tirar suas dúvidas sobre o processamento de pedidos de patentes que foram indeferidos e estão na fase recursal no INPI.  

Informação sobre o processamento em formato JSON: {data}

Seu trabalho é entender a pergunta do examinador por meio de perguntas, para no final indicar a resposta. 

Tenha certeza de perguntar sobre as razões do indeferimento do pedido e se foi apresentado um novo quadro reivindicatório na petição de recurso. 

Quando entender a pergunta do examinador, sugerir o modelo de parecer mais provável a ser usado e o código de despacho mais adequado.

"""

#model = genai.GenerativeModel("gemini-pro") # teste
#response = model.generate_content("O que é uma patente ?")
#st.write(response.text)
#sys.exit(0)

# Inicializa o modelo generativo
model = genai.GenerativeModel(
  model_name="gemini-1.5-pro-latest",
  system_instruction=system_instruction
)

# Mensagem inicial do modelo
initial_model_message = "Olá, eu sou Sophia, um assistente virtual que te ajuda a tirar suas dúvidas sobre o processamento de recursos de pedidos de patente. Como você se chama?"

# Inicializa a conversa do assistente virtual
if "chat_encontra" not in st.session_state:
    st.session_state.chat_encontra = model.start_chat(history=[{'role':'model', 'parts': [initial_model_message]}])

# Título da página
st.title('BatePapo 💬')

# Introdução do assistente virtual
st.write("A Assistente Virtual Sophia está aqui para te ajudar a tirar suas dúvidas sobre o processamento de recursos de paedidos de patente! Atualmente o assistente tem informações mais comuns já cadastradas. Vamos começar?")

# Exibe o histórico de conversa
for i, message in enumerate(st.session_state.chat_encontra.history):
  if message.role == "user":
    with st.chat_message("user"):
      st.markdown(message.parts[0].text)
  else:
    with st.chat_message("assistant"):
      st.markdown(message.parts[0].text)

# Entrada do usuário
user_query = st.chat_input('Você pode falar ou digitar sua resposta aqui:')

# Processamento da entrada do usuário e resposta do assistente
if user_query is not None and user_query != '':
    with st.chat_message("user"):
      st.markdown(user_query)
    with st.chat_message("assistant"):
        ai_query = st.session_state.chat_encontra.send_message(user_query).text
        st.markdown(ai_query)
