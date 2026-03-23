# Constantes
OPERADORES = {"+", "-", "*", "/", "%", "^"}
PARENTESES = {"(", ")"}

def estadoNumero(linha, i):
    """Estado do AFD para reconhecer números reais."""
    numero = []
    tem_ponto = False
    digitos_antes = 0
    digitos_depois = 0

    # suporte a número negativo
    if linha[i] == "-":
        numero.append("-")
        i += 1

    while i < len(linha):
        char = linha[i]

        if char.isdigit():
            numero.append(char)
            if not tem_ponto:
                digitos_antes += 1
            else:
                digitos_depois += 1
            i += 1
            continue

        if char == ".":
            if tem_ponto:
                raise ValueError("Erro léxico: número com múltiplos pontos")
            tem_ponto = True
            numero.append(char)
            i += 1
            continue

        break

    numero_str = "".join(numero)

    # Validações de malformação
    if numero_str in {"", "-"}:
        raise ValueError("Erro léxico: número inválido")

    if tem_ponto and (digitos_antes == 0 or digitos_depois == 0):
        raise ValueError("Erro léxico: número real malformado")

    return numero_str, i


def estadoPalavra(linha, i):
    """Estado do AFD para reconhecer comandos (RES) e identificadores de memória (MEM, VAR, etc)."""
    inicio = i

    while i < len(linha) and linha[i].isalpha():
        i += 1
    
    palavra = linha[inicio:i]

    if not palavra.isupper():
        raise ValueError(f"Erro léxico: palavra deve estar em MAIÚSCULO ({palavra})")
    
    return palavra, i


def estadoOperador(linha, i):
    """Estado do AFD para reconhecer operadores simples e compostos (//)."""
    # operador composto //
    if linha[i:i+2] == "//":
        # valida se não vira "///"
        if i + 2 < len(linha) and linha[i+2] == "/":
            raise ValueError(f"Erro léxico: operador inválido (///)")
        return "//", i + 2

    if linha[i] in OPERADORES:
        return linha[i], i + 1

    raise ValueError(f"Erro léxico: operador inválido ({linha[i]})")

def estadoParenteses(linha, i):
    """Estado do AFD para parênteses."""
    return linha[i], i + 1

def validarEstrutura(tokens):
    """Realiza validações sintáticas básicas requeridas."""
    # 1. Balanço de parênteses
    stack = []
    for token in tokens:
        if token == "(":
            stack.append(token)
        elif token == ")":
            if not stack:
                raise ValueError("Erro sintático: parênteses desbalanceados")
            stack.pop()
    if stack:
        raise ValueError("Erro sintático: parênteses desbalanceados")
    
    # 2. Posicionamento de operadores (Regras RPN básicas para o Lexer)
    for i, token in enumerate(tokens):
        if token in OPERADORES or token == "//":
            if i == 0 or tokens[i - 1] == "(":
                raise ValueError(f"Erro sintático: operador mal posicionado ({token})")
            if i == len(tokens) - 1 and token != tokens[-2]: # Checa se não é o fecha parênteses vindo
                 pass # A lógica RPN (A B op) exige op antes do ')'

def validarTokens(tokens):
    for i, token in enumerate(tokens):

        # operador mal posicionado
        if token in OPERADORES:
            if i == 0 or tokens[i - 1] == "(":
                raise ValueError(f"Erro sintático: operador mal posicionado ({token})")

            if i == len(tokens) - 1:
                raise ValueError(f"Erro sintático: operador no final ({token})")

            if tokens[i + 1] in OPERADORES:
                raise ValueError("Erro sintático: operadores consecutivos")

def parseExpressao(linha):
    """Função principal"""
    tokens = []
    i = 0

    while i < len(linha):
        char = linha[i]

        # ignorar espaços
        if char.isspace():
            i += 1
            continue

        # parênteses
        if char in PARENTESES:
            token, i = estadoParenteses(linha, i)

        # número (inclui negativo)
        elif char.isdigit() or (
            char == "-" and 
            i + 1 < len(linha) and 
            linha[i + 1].isdigit()
        ):
            token, i = estadoNumero(linha, i)

        # palavras (RES, MEM)
        elif char.isalpha():
            token, i = estadoPalavra(linha, i)

        # operadores
        elif char in OPERADORES or char == "/":
            token, i = estadoOperador(linha, i)

        else:
            raise ValueError(f"Erro léxico: caractere inválido ({char})")

        tokens.append(token)

    validarEstrutura(tokens)

    return tokens
