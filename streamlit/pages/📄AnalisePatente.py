import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
import time
from PyPDF2 import PdfReader
import pdfplumber

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

def text_from_pdf_old(pdf):
    text = ""
    pdf_reader = PdfReader(pdf)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def text_from_pdf(pdf):
    text = ""
    with pdfplumber.open(pdf) as pdf_reader:
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
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
    prior_art = st.file_uploader("Upload da anterioridade:", type=['pdf'])

    if prior_art is not None:
        st.write("Qual o idioma original da seção de anterioridade?")
        original_language = st.text_input("Idioma original:", "")
        
        st.write("Há algum ponto específico que você gostaria que eu focasse no resumo?")
        specific_focus = st.text_input("Pontos específicos para focar:", "")

        if original_language and specific_focus:
            with st.spinner('Carregando anterioridade...'):
                prior_art_text = text_from_pdf(prior_art)
            st.success('Anterioridade carregada com sucesso!')

            initial_message_prior_art = (
                f"Olá Sophia, faça o resumo da anterioridade no idioma original ({original_language}) "
                f"e traduza para o português, focando nos seguintes pontos: {specific_focus}. "
                f"Aqui está o texto da anterioridade: {prior_art_text}"
            )
            if st.button('Faça resumo da anterioridade'):
                with st.spinner("Processando..."):
                    ai_query_prior_art = model.generate_content(initial_message_prior_art)
                    st.markdown(ai_query_prior_art.text)

            initial_message_analysis = (
                f"Olá Sophia, aponte as diferenças do pedido com a anterioridade. "
                f"Aqui está o pedido: {patent_text} "
                f"E aqui está a anterioridade: {prior_art_text}"
            )
            if st.button('Faça análise dos documentos'):
                with st.spinner("Processando..."):
                    ai_query_analysis = model.generate_content(initial_message_analysis)
                    st.markdown(ai_query_analysis.text)
        else:
            st.warning('Por favor, preencha o idioma original da anterioridade e os pontos específicos para focar antes de continuar.')
    else:
        st.warning('Por favor, faça o upload da anterioridade antes de continuar.')
else:
    st.warning('Por favor, faça o upload do pedido antes de continuar.')