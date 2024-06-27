import streamlit as st

from pathlib import Path
import sys
import time
from jobs_details import jobs_details as data

from typing import List
import openai
from openai import OpenAI
import os
from dotenv import load_dotenv
import pandas as pd

from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_openai import OpenAIEmbeddings

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY2")
openai.api_key = api_key

# Título da página
st.title('BatePapo 💬')

# Introdução do assistente virtual
st.write("A Assistente Virtual Sophia está aqui para te ajudar a tirar suas dúvidas sobre o processamento de recursos de paedidos de patente! Atualmente o assistente tem informações mais comuns já cadastradas. Vamos começar?")


# Listar todos os arquivos e diretórios no diretório atual
#arquivos = os.listdir('.')
# Filtrar para mostrar apenas arquivos (não diretórios)
#arquivos = [f for f in arquivos if os.path.isfile(f)]
#st.write("Arquivos no diretório atual:")
#for arquivo in arquivos:
#    st.write(arquivo)
  
   
pdf_path = "streamlit/chatbot_cgrec.pdf"  # Especifique o caminho do PDF

# Verificar se o arquivo existe no caminho especificado
if os.path.exists(pdf_path):
    loader = PyPDFLoader(pdf_path)
    st.write("PDF carregado com sucesso!")
else:
    st.error(f"O arquivo {pdf_path} não foi encontrado. Verifique o caminho e tente novamente.")
    
pages = loader.load_and_split()

embeddings = OpenAIEmbeddings(openai_api_key=api_key)

from langchain_community.vectorstores.faiss import FAISS # banco de dados vetorial FAISS
db = FAISS.from_documents(pages, embeddings)

q = "Uma exigência não cumprida na primeira instância sofre preclusão na fase recursal ?"
trecho_relevante = db.similarity_search(q)[0] # ele acessa o texto e localiza trecho relevante

from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain_openai import OpenAI
llm = OpenAI(openai_api_key=api_key)
chain = RetrievalQA.from_llm(llm=llm, retriever=db.as_retriever())
resposta = chain(q, return_only_outputs=True)

st.write(resposta.result)
st.write("=====")
st.write(trecho_relevante.page_content)
st.write("=====")
st.write(trecho_relevante.page)
st.write("=====")