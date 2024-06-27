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

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY2")
openai.api_key = api_key

# Título da página
st.title('BatePapo 💬')

# Introdução do assistente virtual
st.write("A Assistente Virtual Sophia está aqui para te ajudar a tirar suas dúvidas sobre o processamento de recursos de paedidos de patente! Atualmente o assistente tem informações mais comuns já cadastradas. Vamos começar?")

from langchain_community.document_loaders.pdf import PyPDFLoader
loader = PyPDFLoader("chatbot_cgrec.pdf")
pages = loader.load_and_split()

from langchain_openai import OpenAIEmbeddings
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