"""
Gerador de Assembly ARMv7 (CPULATOR) com suporte a IEEE754 64 bits

Integrantes (ordem alfabética):
Murilo Chandelier Pedrazzani - https://github.com/MuriloPedrazzani
Ricardo Ryu Magalhães Makino - https://github.com/ryumakino
Ricardo Vinicius Moreira Vianna - https://github.com/ricaprof

Grupo no Canvas: RA1 8
Disciplina: Construção de Interpretadores
Professor: Frank Alcantara

"""

import sys
from lexer import parseExpressao

testes_passaram = 0

testes_falharam = 0

def testar(expressao, nome="Teste Genérico", deve_erro=False):

    global testes_passaram, testes_falharam

    try:
        tokens = parseExpressao(expressao)
        
        # Caso fosse esperado erro mas não ocorreu
        if deve_erro:
            print(f"[FALHOU] {nome} | {expressao} -> Deveria dar erro, mas passou: {tokens}")
            testes_falharam += 1

        else:
            # Caso esperado sucesso e ocorreu corretamente
            print(f"[OK] {nome} | {expressao} -> {tokens}")
            testes_passaram += 1

    except Exception as e:

        # Caso o erro era esperado
        if deve_erro:
            print(f"[OK - ERRO ESPERADO] {nome} | {expressao} -> {e}")
            testes_passaram += 1

        else:
            # Caso ocorreu erro inesperado
            print(f"[ERRO INESPERADO] {nome} | {expressao} -> {e}")
            testes_falharam += 1

def executar_suite():

    print("=== TESTES BÁSICOS ===")

    # Operações simples validas
    testar("(2 3 +)", nome="Soma Simples")
    testar("(10 5 /)", nome="Divisão Simples")
    testar("(2 3 ^)", nome="Potenciação")


    print("\n=== TESTES COM NEGATIVOS E OPERADORES SOLTOS ===")

    # Testes envolvendo numeros negativos
    testar("(2 - 3)", nome="Subtração clássica")
    testar("(2 -3)", nome="Número negativo literal")
    testar("(-3 2 +)", nome="Número negativo no início")
    testar("(2 (-3) +)", nome="Negativo isolado em parênteses")
    
    # Testes estruturais com operadores
    testar("(-)", nome="Operador solitário")
    testar("(2 - )", nome="Falta operando direito")
    testar("( - 3)", nome="Falta operando esquerdo")


    print("\n=== TESTES DE NÚMEROS ===")

    # Testes com numeros de ponto flutuante
    testar("(1.5 2 +)", nome="Float simples")
    testar("(0.5 3 *)", nome="Float menor que zero")
    testar("(-1.25 4 +)", nome="Float negativo")


    print("\n=== NÚMEROS MALFORMADOS (ERRO LÉXICO ESPERADO) ===")

    # Casos invalidos que devem gerar erro lexico
    testar("(.5 2 +)", nome="Início com ponto", deve_erro=True)
    testar("(5. 2 +)", nome="Término com ponto", deve_erro=True)
    testar("(1..2 3 +)", nome="Múltiplos pontos", deve_erro=True)
    testar("(-.5 2 +)", nome="Sinal seguido de ponto", deve_erro=True)


    print("\n=== TESTES DE PARÊNTESES ===")

    # Testes de balanceamento de parênteses
    testar("(2 3 +", nome="Falta fechar parênteses", deve_erro=True)
    testar("2 3 +)", nome="Falta abrir parênteses", deve_erro=True)
    testar("((2 3 +)", nome="Parênteses desbalanceados", deve_erro=True)


    print("\n=== TESTES DE VARIÁVEIS E COMANDOS ===")

    # Testes relacionados a variaveis e comandos da linguagem
    testar("(ABC 2 +)", nome="Variável válida (Maiúscula)")
    testar("(abc 2 +)", nome="Variável inválida (Minúscula)", deve_erro=True)

    testar("(0 RES)", nome="Comando histórico (RES)")

    testar("(10.5 MEM)", nome="Comando de escrita em memória (MEM)")


    print("\n=== TESTES DE DIVISÃO INTEIRA ===")

    # Testes especificos para operador composto //
    testar("(10 3 //)", nome="Divisão inteira RPN")
    testar("(10 // 3)", nome="Divisão inteira (ordem infixa - válido lexicamente)")


    print("\n=== TESTES COMPLEXOS (ANINHAMENTO) ===")

    # Expressões mais complexas com aninhamento
    testar("((2 3 +) (4 5 *) +)", nome="Aninhamento de operações")
    testar("((2 (-3) +) (10 2 /) *)", nome="Aninhamento com negativos e divisão")


    print("\n=== TESTES DE ESTRUTURA (RPN INVÁLIDA MAS LEXICAMENTE OK) ===")

    testar("(2 3 + +)", nome="Excesso de operadores")


    print("\n=== TESTES DE CARACTERES E OPERADORES INVÁLIDOS (ERRO LÉXICO ESPERADO) ===")

    # Testes com caracteres que não pertencem à linguagem
    testar("(2 3 &)", nome="Caractere especial &", deve_erro=True)
    testar("(2 3 @)", nome="Caractere especial @", deve_erro=True)
    testar("(2 3_ +)", nome="Underscore", deve_erro=True)
    testar("(2 /* 3)", nome="Operador composto inválido (/*)", deve_erro=True)
    

    print("\n=== TESTES DE BOUNDARY E EDGE CASES (ERRO ESPERADO / TRATAMENTO DE ESPAÇOS) ===")

    # Testes de tokens colados ou falta de separação
    testar("(123abc)", nome="Tokens colados (Número + Letra)", deve_erro=True)
    testar("(123+abc)", nome="Tokens colados sem espaço", deve_erro=True)
    testar("(2///3)", nome="Operadores excessivos colados (///)", deve_erro=True)

    # Teste de trim de espaços
    testar("   (2 3 +)   ", nome="Espaços no início e fim (Trim test)")
    

    print("\n=== TESTE DE CARGA ===")

    # Teste de estresse com muitos literais
    expressao_gigante = "(" + " ".join(["1.0"] * 100) + " +)"
    testar(expressao_gigante, nome="Stress Test (100 literais)")


if __name__ == "__main__":

    # Executa toda a suite de testes
    executar_suite()
    
    print("\n" + "="*50)
    print("SUMÁRIO DE TESTES LÉXICOS")
    print("="*50)

    print(f"Passaram: {testes_passaram}")
    print(f"Falharam: {testes_falharam}")

    print("="*50)

    if testes_falharam > 0:
        sys.exit(1)
    else:
        sys.exit(0)
