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

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

st.title('FAQ ❓')
st.write("Envie o pedido de patente.")
st.write(f"perguntas = {data}")