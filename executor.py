import math

memoria = {}

historico = []


# função auxiliar para verificar se um token é numero
def isNumero(token):
    try:
        float(token)
        return True
    except ValueError:
        return False


# utiliza uma pilha para avaliar os tokens
def executarExpressao(tokens):

    stack = []

    for i, token in enumerate(tokens):

        # ignora parenteses
        if token in ("(", ")"):
            continue

        if isNumero(token):
            stack.append(float(token))
            continue

        if token in ("+", "-", "*", "/", "//", "%", "^"):

            # verifica se existem operandos suficientes
            if len(stack) < 2:
                raise ValueError("Erro: operandos insuficientes")

            b = stack.pop()
            a = stack.pop()

            if token == "+":
                resultado = a + b

            elif token == "-":
                resultado = a - b

            elif token == "*":
                resultado = a * b

            elif token == "/":
                if b == 0:
                    raise ValueError("Erro: divisão por zero")
                resultado = a / b

            elif token == "//":
                if b == 0:
                    raise ValueError("Erro: divisão inteira por zero")
                resultado = int(a) // int(b)

            elif token == "%":
                if b == 0:
                    raise ValueError("Erro: resto de divisão por zero")
                resultado = int(a) % int(b)

            elif token == "^":

                expoente = int(b)

                if expoente < 0:
                    raise ValueError("Erro: expoente negativo")

                resultado = a ** expoente

            stack.append(resultado)
            continue

        # permite acessar resultados anteriores
        if token == "RES":

            if len(stack) < 1:
                raise ValueError("Erro: RES sem argumento")

            valor = stack.pop()

            if not float(valor).is_integer():
                raise ValueError("Erro: argumento de RES deve ser inteiro")

            n = int(valor)

            if n <= 0 or n > len(historico):
                raise ValueError(f"Erro: índice inválido para RES ({n})")

            stack.append(historico[-n])
            continue

        if token.isalpha():

            # verifica se esta lendo ou gravando na variável
            is_read = (i > 0 and tokens[i - 1] == "(")

            if is_read:
                stack.append(memoria.get(token, 0.0))

            else:

                if len(stack) == 0:
                    raise ValueError(f"Erro: memória vazia para '{token}'")

                val = stack.pop()
                memoria[token] = val
                stack.append(val)

            continue

        raise ValueError(f"Token inválido: {token}")

    if len(stack) != 1:
        raise ValueError("Erro: expressão malformada")

    resultado = stack.pop()

    if not isinstance(resultado, float):
        resultado = float(resultado)

    # evita resultados invalidos
    if math.isnan(resultado) or math.isinf(resultado):
        raise ValueError("Erro: resultado numérico inválido")

    # salva resultado no histórico
    historico.append(resultado)

    return resultado