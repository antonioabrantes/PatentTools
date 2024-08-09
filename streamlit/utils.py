import os
import re
# https://www.youtube.com/watch?v=JbiTQVKvNew&t=597s
# Fazendo um Sistema de Agentes com I.A do Zero Sem CrewAI
# https://github.com/inteligenciamilgrau/videos_tutoriais/tree/main/crewai_sem_crewai

import requests
import json
from dotenv import load_dotenv

# Load environment variables from .env file
app_dir = os.path.join(os.getcwd(), "app")
load_dotenv(os.path.join(app_dir, ".env"))

def send_message(prompt, sistema = "", json_format = False):

    api_key = os.getenv("OPENAI_API_KEY")  # Get the API key from the environment
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    formato = "text"
    if json_format:
        formato = "json_object"

    mensagem = []
    if sistema != "":
        mensagem.append({"role": "system", "content": sistema})
    mensagem.append({"role": "user", "content": prompt})

    data = {
        "model": "gpt-3.5-turbo",  # Ensure to specify the correct model
        "messages": mensagem,
        "max_tokens": 512,  # You can adjust this as needed
        "response_format": { "type": formato },
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        response_json = response.json()
        if json_format:
            return json.loads(response_json['choices'][0]['message']['content'])
        return response_json['choices'][0]['message']['content']
    else:
        st.write(f"Error: {response.status_code}, {response.text}")
        return None
        
#Patentes de Invenção: 
#10 – para pedidos depositados por nacionais e via CUP (antigo PI); 
#11 – para pedidos depositados via PCT (antigo PI PCT); 
#12 – para pedidos divididos (antigo PI); 
#13 – para certificado de adição (antigo C1, C2, etc). 
#Patentes de Modelo de Utilidade: 
#20 – para pedidos depositados por nacionais e via CUP (antigo MU); 
#21 – para pedidos depositados via PCT (antigo MU PCT); 
#22 – para pedidos divididos (antigo MU).


def extrair_digito_verificador(numero_pedido):
    # Remover espaços e prefixo "BR" se presente
    numero_pedido = numero_pedido.strip().replace(" ", "").upper()
    
    # Encontrar a posição do hífen e extrair o dígito verificador
    if '-' in numero_pedido:
        partes = numero_pedido.split('-')
        if len(partes) == 2 and len(partes[1]) == 1 and partes[1].isdigit():
            digito_verificador = partes[1]
        else:
            return -1 # ("O formato do número do pedido está incorreto.")
    else:
        return -2 # ("O número do pedido não contém um hífen com o dígito verificador.")
    
    return int(digito_verificador)
    
    
def calcular_digito_verificador(numero_pedido):
    # Remover espaços e juntar os números do pedido em uma única string
    numero_pedido = ''.join(numero_pedido.split())

    numero_pedido = numero_pedido.replace(" ", "").upper().strip()

    prefixos = ("BR", "PI", "MU", "C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9")
    if numero_pedido.startswith(prefixos):
        numero_pedido = numero_pedido[2:]
        
    digito_verificador = -1

    numero_pedido = numero_pedido.split('-')[0] # ignore o que ve depois do hofen, se houver
    
    # Verificar se o número tem o formato correto (12 dígitos)
    if len(numero_pedido) == 12 and numero_pedido.isdigit():

        prefixos = ("10", "11", "12", "13", "20", "21", "22")
        if not numero_pedido.startswith(prefixos):
            return -2

        # https://www.uece.br/agin/noticias/inpi-veja-como-calcular-o-digito-verificador-na-nova-numeracao-da-dirpa-e-da-dicig/
        # Inverter o número do pedido
        numero_invertido = numero_pedido[::-1]
        
        # Inicializar variáveis
        soma = 0
        multiplicador = 2
        
        # Calcular soma dos produtos dos dígitos pelo multiplicador
        for digito in numero_invertido:
            soma += int(digito) * multiplicador
            multiplicador += 1
            if multiplicador > 9:
                multiplicador = 2
        
        # Calcular o resto da divisão da soma por 11
        resto = soma % 11
        
        # Calcular o dígito verificador
        digito_verificador = 11 - resto
        if digito_verificador == 10 or digito_verificador == 11:
            digito_verificador = 0

    if len(numero_pedido) == 7 and numero_pedido.isdigit():
        
        # Inverter o número do pedido
        numero_invertido = numero_pedido[::-1]
        
        # Inicializar variáveis
        soma = 0
        multiplicador = 2
        
        # Calcular soma dos produtos dos dígitos pelo multiplicador
        for digito in numero_invertido:
            soma += int(digito) * multiplicador
            multiplicador += 1
            if multiplicador > 9:
                multiplicador = 2
        
        # Calcular o resto da divisão da soma por 11
        resto = soma % 11
        
        # Calcular o dígito verificador
        digito_verificador = 11 - resto
        if digito_verificador == 10 or digito_verificador == 11:
            digito_verificador = 0

        #digito_verificador = -3

    return digito_verificador
    
import requests
from datetime import datetime

month_names = {
    1: "janeiro",
    2: "fevereiro",
    3: "março",
    4: "abril",
    5: "maio",
    6: "junho",
    7: "julho",
    8: "agosto",
    9: "setembro",
    10: "outubro",
    11: "novembro",
    12: "dezembro"
}

def convert_date(date_str):
    # Parse the date string
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    
    # Extract the day, month, and year
    day = date_obj.day
    month = month_names[date_obj.month]
    year = date_obj.year
    
    # Format the date in the desired format
    formatted_date = f"{day} de {month} de {year}"
    return formatted_date
    
# Definindo cabeçalhos para a requisição
headers = {
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}


def acessar_sinergias(url):
    try:
        # Requisição para obter os dados JSON
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Verificar se a requisição foi bem-sucedida
    
        # Tentar decodificar o JSON
        data = response.json()
        #print(data)
    
        # Carregar os dados JSON em um DataFrame
        #df = pd.DataFrame(data['despacho'])
        #df['despacho'] = df['despacho'].fillna('Unknown')
    
        #print(df)
    
        # Verificar e converter a coluna 'count' para inteiro
        #df['tempo'] = pd.to_numeric(df['tempo'], errors='coerce')
        return data
    
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Error occurred during request: {req_err}")
    except ValueError as json_err:
        print(f"JSON decode error: {json_err}")
    except Exception as err:
        print(f"An unexpected error occurred: {err}")    
    return -1
    
# teste expressão regular online

def extrair_numero_pedido(texto):
    padrao = r"(PI|MU|C1|C2|C3|C4|C5|C6|C7|C8|C9)\s*\d{7}(?:-\d)?|(?:BR\s*)?(?:\d{2}\s*)?(?:\d{4}\s*)?\d{6}(?:-\d)?"
    match = re.search(padrao, texto)
    if match:
        numero_pedido = match.group()
        numero_pedido = numero_pedido.replace(" ", "").upper().strip()
        return numero_pedido
    else:
        return None

