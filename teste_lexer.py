from lexer import parseExpressao

def testar_entradas_validas():

    print("Testando entradas válidas:\n")

    # Lista de expressões consideradas validas na linguagem
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
        "(-7 3 %)",    
        "(2 -3 ^)"    
    ]

    aprovados = 0

    # Executa o lexer para cada expressão
    for teste in testes:
        try:
            tokens = parseExpressao(teste)

            # Caso funcione corretamente, imprime os tokens gerados
            print(f"✓ '{teste}' -> {tokens}")
            aprovados += 1

        except Exception as e:
            # Caso ocorra erro em uma entrada valida, isso indica problema no lexer
            print(f"✗ '{teste}' -> Erro inesperado: {e}")

    # Mostra quantos testes validos passaram
    print(f"\n{aprovados}/{len(testes)} testes válidos passaram.\n")


def testar_entradas_invalidas():


    print("Testando entradas inválidas:\n")

    testes = [
        "(3.14.5 2.0 +)",  
        "(3,45 2.0 +)",    
        "(3.14 2.0 &)",  
        "(3.14 2.0 +",    
        "(3.14 @ 2.0 +)",  
        ")3.14 2.0 +(",   
        "(var 2.0 +)",   
        "(True 2 +)",     
        "(False 2 +)",   
        "(None 2 +)"       
    ]

    aprovados = 0

    # Executa o lexer para cada caso invalido
    for teste in testes:
        try:
            tokens = parseExpressao(teste)

            print(f"✗ '{teste}' -> {tokens} (deveria falhar)")

        except Exception as e:
            print(f"✓ '{teste}' -> Erro esperado: {e}")
            aprovados += 1

    # Mostra quantos erros foram detectados corretamente
    print(f"\n{aprovados}/{len(testes)} testes inválidos detectados.\n")


if __name__ == "__main__":

    testar_entradas_validas()

    print("-" * 40 + "\n")

    testar_entradas_invalidas()
