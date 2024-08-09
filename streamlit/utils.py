

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
