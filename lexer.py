def estadoNumero(linha, i):
    numero = ""
    tem_ponto = False
    digitos_antes = 0
    digitos_depois = 0

    # suporte a número negativo
    if linha[i] == "-":
        numero += "-"
        i += 1

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
                raise ValueError("Número malformado: múltiplos pontos")
            tem_ponto = True
            numero += char
            i += 1
            continue

        break

    if numero == "-" or numero == "":
        raise ValueError("Número inválido")

    if tem_ponto and (digitos_antes == 0 or digitos_depois == 0):
        raise ValueError("Número real inválido")

    return numero, i


def estadoPalavra(linha, i):
    palavra = ""

    while i < len(linha) and linha[i].isalpha():
        palavra += linha[i]
        i += 1

    if not palavra.isupper():
        raise ValueError(f"Palavra inválida (use MAIÚSCULO): {palavra}")

    return palavra, i


def estadoOperador(linha, i):
    operadores = {"+", "-", "*", "/", "%", "^"}

    # operador composto //
    if linha[i:i+2] == "//":
        return "//", i + 2

    if linha[i] in operadores:
        return linha[i], i + 1

    raise ValueError(f"Operador inválido: {linha[i]}")


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

        elif char.isdigit() or (char == "-" and i + 1 < len(linha) and linha[i+1].isdigit()):
            token, i = estadoNumero(linha, i)

        elif char.isalpha():
            token, i = estadoPalavra(linha, i)

        elif char in "+-*/%^":
            token, i = estadoOperador(linha, i)

        else:
            raise ValueError(f"Caractere inválido: {char}")

        tokens.append(token)

    validarParenteses(tokens)
    return tokens
