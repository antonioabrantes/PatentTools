import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
import time
from PyPDF2 import PdfReader
import pdfplumber
from urllib.request import urlopen
from bs4 import BeautifulSoup

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
Seu nome é Sophia, uma assistente virtual que ajuda um examinador de patentes a analisar um documento em PDF carregado pelo usuário.
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

# View all key:value pairs in the session state
def view_session_state():
    s = []
    for k, v in st.session_state.items():
        s.append(f"{k}: {v}")
    st.write(s)

# Função para resetar o estado da sessão
def reset_session_state():
    for key in st.session_state.keys():
        # del st.session_state[key]
        st.write(key)

# Botão para resetar a aplicação
if st.button("Resetar aplicação"):
    reset_session_state()
    st.experimental_rerun()
    
view_session_state()

# Upload do currículo
st.write("Por favor, faça o upload do pedido em formato PDF")
pedido = st.file_uploader("Upload do pedido:", type=['pdf'])
if pedido is not None:
    if 'patent_text' not in st.session_state:
        with st.spinner('Carregando pedido...'):
            st.session_state.patent_text = text_from_pdf(pedido)
        st.success('Pedido carregado com sucesso!')
        
    st.write("Há algum tema específico que você gostaria que eu focasse no resumo?")
    st.session_state.specific_focus = st.text_input("Pontos específicos para focar:", "")
    if 'specific_focus' in st.session_state:
        st.markdown(f"**Tema específico:**\n\n{st.session_state.specific_focus}")
    
    messagem_resumo = (
        f"Olá Sophia, faça o resumo do documento em português {st.session_state.patent_text} "
        f" focando nos seguintes pontos: {st.session_state.specific_focus}. "
    )
    if st.button('Faça resumo do documento'):
        if 'abstract' not in st.session_state:
            with st.spinner("Processando..."):
                st.session_state.abstract = model.generate_content(messagem_resumo).text
        st.markdown(f"**Resumo:**\n\n{st.session_state.abstract}")

        st.write("Digite o número do documento de patente:")
        numero = st.text_input("Número:", "")
        
        if st.button('Acesse google patents para buscar esta patente'):
            abstract = ''
            title = ''
            html = urlopen('https://patents.google.com/patent/US5000000A/en?oq=US5000000')
            bs = BeautifulSoup(html.read(),'html.parser')
            title = bs.title.get_text()
            nameList = bs.findAll("div",{"class":"abstract"})
            for name in nameList:
                abstract = name.getText()
            st.markdown(f"**Título:**\n\n{title}")
            st.markdown(f"**Resumo:**\n\n{abstract}")

            #initial_message_analysis = (
            #    f"Olá Sophia, aponte as diferenças do pedido com a anterioridade. "
            #    f"Aqui está o pedido: {patent_text} "
            #    f"E aqui está a anterioridade: {prior_art_text}"
            #)
            #if st.button('Faça análise dos documentos'):
            #    with st.spinner("Processando..."):
            #        ai_query_analysis = model.generate_content(initial_message_analysis)
            #        st.markdown(ai_query_analysis.text)
else:
    st.warning('Por favor, faça o upload do pedido antes de continuar.')