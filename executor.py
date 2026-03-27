def isNumero(token):

    try:
        float(token)
        return True
    except ValueError:
        return False

def aplicar_operacao(op, a, b):

    if op == "+":
        return a + b

    elif op == "-":
        return a - b

    elif op == "*":
        return a * b

    elif op == "/":

        if b == 0:
            raise ZeroDivisionError("Divisão por zero")
        return a / b

    elif op == "//":

        if b == 0:
            raise ZeroDivisionError("Divisão inteira por zero")
        return a // b

    elif op == "%":

        if b == 0:
            raise ZeroDivisionError("Módulo por zero")
        return a % b

    elif op == "^":

        if not float(b).is_integer() or b < 0:
            raise ValueError("O expoente da potenciação deve ser um inteiro positivo")

        return a ** int(b)

    else:

        raise ValueError(f"Operador inválido: {op}")

def executarExpressao(tokens, historico, memoria):

    stack = []

    # Percorre todos os tokens da expressão
    for i, token in enumerate(tokens):

        if token in ("(", ")"):
            continue

        if isNumero(token):
            stack.append(float(token))

        # Qualquer palavra maiuscula (exceto RES) é considerada variavel
        elif isinstance(token, str) and token.isalpha() and token != "RES":

            if i > 0 and tokens[i - 1] == "(":

                valor = memoria.get(token, 0.0)
                stack.append(valor)

            else:
                if not stack:
                    raise ValueError("Sem valor na pilha para armazenar na memória")

                valor = stack.pop()
                memoria[token] = valor
                stack.append(valor)

        elif token == "RES":

            # Precisa existir um valor na pilha indicando quantas linhas voltar
            if not stack:
                raise ValueError("RES sem valor de N na pilha")

            valor_n = stack.pop()

            # Valida se o valor é inteiro não negativo
            if not float(valor_n).is_integer() or valor_n < 0:
                raise ValueError("RES exige inteiro não negativo")

            n = int(valor_n)

            # Verifica se existe historico suficiente
            if n >= len(historico):
                raise ValueError(f"Linha de histórico inacessível para {n} RES")

            resultado_historico = historico[-(n + 1)]
            stack.append(resultado_historico)

        else:

            # Operações matematicas exigem dois operandos
            if len(stack) < 2:
                raise ValueError(f"Operandos insuficientes para operador '{token}'")

            b = stack.pop()
            a = stack.pop()

            # Executa a operação e empilha o resultado
            resultado = aplicar_operacao(token, a, b)
            stack.append(resultado)

    if len(stack) != 1:
        raise ValueError("Expressão mal formada (sobraram valores na pilha)")

    return stack[0]