from lexer import parseExpressao


def testar_entradas_validas():
    print("Testando entradas válidas:\n")

    testes = [
        "(3.14 2.0 +)",
        "(5 RES)",
        "(10.5 CONTADOR)",
        "(1.0 2.0 *)",
        "((3.0 4.0 +) 2.0 /)",
        "(10 3 //)",
        "(10 3 %)",
        "(2 3 ^)",
        "(4.5 2.0 -)",
        "(VARIAVEL 5 +)",
        "(-3.5 2 +)",
        "(0.5 1.5 +)",
        "(100 200 +)",
        "(A B +)"
    ]

    for teste in testes:
        try:
            tokens = parseExpressao(teste)
            print(f"✓ {teste} -> {tokens}")
        except Exception as e:
            print(f"✗ {teste} -> ERRO: {e}")


def testar_entradas_invalidas():
    print("\nTestando entradas inválidas:\n")

    testes = [
        "(3.14.5 2.0 +)",
        "(3,45 2.0 +)",
        "(3.14 2.0 &)",
        "(3.14 2.0 +",
        ")3.14 2.0 +(",
        "(3.14 @ 2.0 +)",
        "(var 2.0 +)",
        "(- 3.5 2 +)",          # negativo mal formado
        "(3. 2 +)",             # decimal inválido
        "(.5 2 +)",             # decimal inválido
        "(A1 2 +)",             # palavra inválida
        "(10 2 ///)",           # operador inválido
    ]

    for teste in testes:
        try:
            tokens = parseExpressao(teste)
            print(f"✗ {teste} -> passou errado: {tokens}")
        except Exception as e:
            print(f"✓ {teste} -> erro esperado: {e}")


if __name__ == "__main__":
    testar_entradas_validas()
    print("\n" + "-" * 40)
    testar_entradas_invalidas()
