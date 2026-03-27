def estadoNumero(linha, i):


    numero = ""
    tem_ponto = False
    digitos_antes = 0
    digitos_depois = 0

    # Trata o caso de numero negativo
    if linha[i] == "-":
        numero += "-"
        i += 1

        if i >= len(linha) or not linha[i].isdigit():
            raise ValueError("Número negativo malformado")

    # Loop que percorre os caracteres do numero
    while i < len(linha):
        char = linha[i]

        if char.isdigit():
            numero += char

            # Contamos quantos digitos existem antes e depois do ponto
            if not tem_ponto:
                digitos_antes += 1
            else:
                digitos_depois += 1

            i += 1
            continue

        if char == ".":
            if tem_ponto:
                raise ValueError("Número malformado")

            tem_ponto = True
            numero += char
            i += 1
            continue

        break

    # Validação para garantir formato correto de numero real
    if tem_ponto and (digitos_antes == 0 or digitos_depois == 0):
        raise ValueError("Número real inválido")

    return numero, i

def estadoPalavra(linha, i):

    palavra = ""

    while i < len(linha) and linha[i].isalpha():
        palavra += linha[i]
        i += 1

    # A linguagem exige que variaveis e comandos sejam em MAIUSCULO
    if not palavra.isupper():
        raise ValueError(f"Variável/Comando inválido (deve ser maiúsculo): {palavra}")

    return palavra, i


def estadoOperador(linha, i):


    char = linha[i]

    if char == "/" and i + 1 < len(linha) and linha[i + 1] == "/":
        return "//", i + 2

    # Operadores simples suportados pela linguagem
    if char in "+-*/%^":
        return char, i + 1

    # Qualquer outro símbolo é invalido
    raise ValueError(f"Operador inválido: {char}")

def estadoParenteses(linha, i):

    return linha[i], i + 1


def validarParenteses(tokens):


    stack = []

    for t in tokens:
        if t == "(":
            stack.append(t)

        elif t == ")":
            if not stack:
                raise ValueError("Parênteses desbalanceados")

            stack.pop()

    # Se sobrar algo na pilha significa que faltou fechar
    if stack:
        raise ValueError("Parênteses desbalanceados")


def parseExpressao(linha):

    tokens = []
    i = 0

    while i < len(linha):
        char = linha[i]

        # Ignora espaços em branco
        if char.isspace():
            i += 1
            continue

        if char in "()":
            token, i = estadoParenteses(linha, i)
            tokens.append(token)
            continue

        # Verifica se é numero ou numero negativo
        if char.isdigit() or (char == "-" and i + 1 < len(linha) and linha[i + 1].isdigit()):
            token, i = estadoNumero(linha, i)
            tokens.append(token)
            continue

        if char.isalpha():
            token, i = estadoPalavra(linha, i)
            tokens.append(token)
            continue


        if char in "+-*/%^":
            token, i = estadoOperador(linha, i)
            tokens.append(token)
            continue

        # Caso encontre qualquer caractere invalido
        raise ValueError(f"Caractere inválido: {char}")

    validarParenteses(tokens)

    return tokens
