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

#from langchain_community.document_loaders.pdf import PyPDFLoader
#from langchain_openai import OpenAIEmbeddings

import PyPDF2
import os
import pandas as pd
from elevenlabs import play, save, Voice, VoiceSettings
from elevenlabs.client import ElevenLabs
import pygame

from transformers import GPT2TokenizerFast
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.chains import ConversationalRetrievalChain

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY2")
openai.api_key = api_key

chave_eleven = os.getenv("ELEVENLABS_API_KEY")
client = ElevenLabs(
  api_key=chave_eleven  # Defaults to ELEVEN_API_KEY
)

pygame.mixer.init()

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
    st.write("Arquivo chatbot_cgrec.pdf carregado com sucesso!")
else:
    st.error(f"O arquivo {pdf_path} não foi encontrado. Verifique o caminho e tente novamente.")
    
# Abrir o arquivo PDF
with open(pdf_path, "rb") as file:
    reader = PyPDF2.PdfReader(file)
    num_pages = len(reader.pages)
    
    all_text = ""
    
    for page_num in range(num_pages):
        page = reader.pages[page_num]
        text = page.extract_text()
        if text:
            all_text += text
    
    # Salvar todo o texto em um arquivo
    #with open("bitcoin.txt", "w", encoding="utf-8") as output_file:
    #    output_file.write(all_text)
    
# st.write(all_text)
text = all_text

tokenizer = GPT2TokenizerFast.from_pretrained("gpt2", use_ssl=False)  # este gpt2 é gratuito para calcular número de tokens, não precisa de api_key

def count_tokens(text: str) -> int:
    return len(tokenizer.encode(text))

text_splitter = RecursiveCharacterTextSplitter( # divide o PDF em blocos/chunks de 512 tokens
    chunk_size = 512,
    chunk_overlap  = 24,
    length_function = count_tokens,
)

chunks = text_splitter.create_documents([text])

embeddings = OpenAIEmbeddings(openai_api_key=api_key, model="text-embedding-ada-002")

db = FAISS.from_documents(chunks, embeddings)

query = "Na segunda instância existe prescrição para uma exigência técnica não cumprida na primeira instância?"
docs = db.similarity_search(query)
# st.write(docs[0].page_content)

llm = OpenAI(openai_api_key=api_key, temperature=0)
chain = load_qa_chain(llm, chain_type="stuff")
# resposta = chain.run(input_documents=docs, question=query)    
# st.write(query)
# st.write(resposta)

#retriever=db.as_retriever()
#chain = RetrievalQA.from_chain_type(llm, retriever=retriever)

# Inicializa a conversa do assistente virtual
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    
# Exibe o histórico de conversa
for message in st.session_state.chat_history:
    if message['role'] == "user":
        with st.chat_message("user"):
            st.markdown(message['content'])
    else:
        with st.chat_message("assistant"):
            st.markdown(message['content'])

# Entrada do usuário
user_query = st.chat_input('Você pode falar ou digitar sua resposta aqui:')

# Processamento da entrada do usuário e resposta do assistente
if user_query is not None and user_query != '':
    # Adiciona a mensagem do usuário ao histórico
    st.session_state.chat_history.append({'role': 'user', 'content': user_query})
    
    # Exibe a mensagem do usuário
    with st.chat_message("user"):
        st.markdown(user_query)

    # Processa a mensagem do usuário e gera a resposta
    resposta = chain.run(input_documents=docs, question=user_query)
    
    # Adiciona a resposta do assistente ao histórico
    st.session_state.chat_history.append({'role': 'assistant', 'content': resposta})
    
    # Exibe a resposta do assistente
    with st.chat_message("assistant"):
        st.markdown(resposta)
        
        voice='TX3LPaxmHKxFdv7VOQHJ'
        audio = client.generate(
            text='testando',
            voice=Voice(voice_id=voice,
                        settings=VoiceSettings(stability=0.35,
                                               similarity_boost=0.4,
                                               style=0.55,
                                               use_speaker_boost=False)),
            model='eleven_multilingual_v2'
        )
        
        filename = "./resposta.mp3"
        #save(audio=audio,filename=filename)
        #filename = os.path.abspath(filename)
        #playsound(filename)
        
        if not os.path.exists(filename):
            save(audio=audio, filename=filename)
        filename = os.path.abspath(filename)
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

# pages = loader.load_and_split()

# embeddings = OpenAIEmbeddings(openai_api_key=api_key)

# from langchain_community.vectorstores.faiss import FAISS # banco de dados vetorial FAISS
# db = FAISS.from_documents(pages, embeddings)

# q = "Uma exigência não cumprida na primeira instância sofre preclusão na fase recursal ?"
# trecho_relevante = db.similarity_search(q)[0] # ele acessa o texto e localiza trecho relevante

# from langchain.chains.retrieval_qa.base import RetrievalQA
# from langchain_openai import OpenAI
# llm = OpenAI(openai_api_key=api_key)
# chain = RetrievalQA.from_llm(llm=llm, retriever=db.as_retriever())
# resposta = chain(q, return_only_outputs=True)

# st.write(resposta.result)
# st.write("=====")
# st.write(trecho_relevante.page_content)
# st.write("=====")
# st.write(trecho_relevante.page)
# st.write("=====")

