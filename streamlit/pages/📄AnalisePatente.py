import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
import time
from PyPDF2 import PdfReader

from pathlib import Path
import hashlib

# https://share.streamlit.io/
load_dotenv()
# Obtém a chave da API da variável de ambiente
# no streamlit https://share.streamlit.io/ escolha o app / Settings / Secrets e guarde a chave API do Google
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Carregando as instruções do sistema para o Gemini
system_instruction = """
Seu nome é Sophia, uma assistente virtual que ajuda um examinador de patentes a analisar um pedido de patente.
Você deve fornecer o resumo do pedido de patente enviado em formato PDF.
"""

# Inicializando o modelo Gemini (gemini-1.5-pro-latest)
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest",
    system_instruction=system_instruction
)

def text_from_pdf(pdf):
    text = ""
    pdf_reader = PdfReader(pdf)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Título da página
st.title('AnalisePatente 📄')
st.write("Envie o pedido de patente.")

# Upload do currículo
st.write("Por favor, faça o upload do pedido em formato PDF")
pedido = st.file_uploader("Upload do pedido:", type=['pdf'])
if pedido is not None:
    with st.spinner('Carregando pedido...'):
        text = text_from_pdf(pedido)
    st.success('Pedido carregado com sucesso!')
    
    initial_message = f"Olá Sophia, faça o resumo do pedido {text}."
    if st.button('Faça resumo do pedido'):
        with st.spinner("Processando..."):
            ai_query = model.generate_content(initial_message)
            st.markdown(ai_query.text)

    st.write("Envie a anterioridade.")
    st.write("Por favor, faça o upload da anterioridade em formato PDF")
    
    prior_art = st.file_uploader("Upload da anterioridade:", type=['pdf'])
    if prior_art is not None:
        with st.spinner('Carregando anterioridade...'):
            text_anterioridade = text_from_pdf(prior_art)
        st.success('Anterioridade carregada com sucesso!')

        initial_message = f"Olá Sophia, faça o resumo da anterioridade e traduza para o português {text_anterioridade}."
        if st.button('Faça resumo da anterioridade'):
            with st.spinner("Processando..."):
                ai_query_anterioridade = model.generate_content(initial_message)
                st.markdown(ai_query_anterioridade.text)

        initial_message = f"Olá Sophia, aponte as diferenças do primeiro PDF carregado com o segundo PDF carregado."
        if st.button('Faça análise dos documentos'):
            with st.spinner("Processando..."):
                ai_query_analise = model.generate_content(initial_message)
                st.markdown(ai_query_analise.text)

    else:
        st.warning('Por favor, faça o upload da anterioridade antes de continuar.')
else:
    st.warning('Por favor, faça o upload do pedido antes de continuar.')
