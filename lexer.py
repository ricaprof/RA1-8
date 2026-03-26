def estadoNumero(linha, i):
    numero = ""
    tem_ponto = False
    digitos_antes = 0
    digitos_depois = 0

    # percorre os caracteres enquanto fizerem parte do numero
    while i < len(linha):
        char = linha[i]

        if char.isdigit():
            numero += char
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

    # valida numeros reais garantindo digitos antes e depois do ponto
    if tem_ponto and (digitos_antes == 0 or digitos_depois == 0):
        raise ValueError("Número real inválido")

    return numero, i


def estadoPalavra(linha, i):
    palavra = ""

    while i < len(linha) and linha[i].isalpha():
        palavra += linha[i]
        i += 1

    # verifica se está em maiusculo
    if not palavra.isupper():
        raise ValueError(f"Variável/Comando inválido (deve ser maiúsculo): {palavra}")

    return palavra, i


# Identifica operadores matematicos da linguagem
def estadoOperador(linha, i):
    char = linha[i]

    if char == "/" and i + 1 < len(linha) and linha[i + 1] == "/":
        return "//", i + 2

    if char in "+-*/%^":
        return char, i + 1

    raise ValueError(f"Operador inválido: {char}")


# Apenas retorna o parentese encontrado e avança a leitura
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

    if stack:
        raise ValueError("Parênteses desbalanceados")



# Função principal do lexer
def parseExpressao(linha):
    tokens = []
    i = 0

    while i < len(linha):
        char = linha[i]

        if char.isspace():
            i += 1
            continue

        if char in "()":
            token, i = estadoParenteses(linha, i)
            tokens.append(token)
            continue

        if char.isdigit():
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

        raise ValueError(f"Caractere inválido: {char}")

    validarParenteses(tokens)

    return tokens
