import sys
from lexer import parseExpressao
from executor import executarExpressao
from assembly import gerarAssembly


# Função responsavel por ler o arquivo de entrada
def lerArquivo(nomeArquivo):
    try:
        with open(nomeArquivo, "r") as arquivo:
            return arquivo.readlines()
    except FileNotFoundError:
        print(f"Erro: O arquivo '{nomeArquivo}' não foi encontrado.")
        sys.exit(1)


# Salva os tokens gerados pelo lexer em um arquivo
def salvarTokens(tokens):
    try:
        with open("tokens.txt", "w") as arquivo:
            for token in tokens:
                arquivo.write(str(token) + "\n")
    except Exception as e:
        print(f"Erro ao salvar tokens: {e}")


# Salva o codigo assembly gerado em um arquivo
def salvarAssembly(codigo):
    try:
        with open("program.s", "w") as arquivo:
            if isinstance(codigo, list):
                arquivo.write("\n".join(codigo) + "\n")
            else:
                arquivo.write(str(codigo) + "\n")
    except Exception as e:
        print(f"Erro ao salvar assembly: {e}")


# Exibe os resultados das expressões executadas
def exibirResultados(resultados):
    if not resultados:
        print("\nNenhuma expressão válida foi executada.")
        return

    print("\nResultados:")
    for linha, resultado in resultados:
        print(f"Linha {linha}: {resultado}")


# Controla todo o fluxo da aplicação
def main():
    if len(sys.argv) < 2:
        print("Uso: python main.py teste1.txt")
        sys.exit(1)

    nomeArquivo = sys.argv[1]

    # lê todas as linhas do arquivo
    linhas = lerArquivo(nomeArquivo)

    resultados = []
    linha_atual = 1

    # guarda tokens da ultima execução
    tokensUltimaExecucao = []

    # guarda tokens de todas as expressões validas
    linhas_tokens = []

    for linha in linhas:

        linha = linha.strip()

        # ignora linhas vazias
        if not linha:
            linha_atual += 1
            continue

        try:
            # executa o lexer
            tokens = parseExpressao(linha)

            # executa a expressão usando o executor
            resultado = executarExpressao(tokens)

            resultados.append((linha_atual, resultado))

            tokensUltimaExecucao = tokens
            linhas_tokens.append(tokens)

        except Exception as e:
            print(f"Erro na linha {linha_atual}: {e}")

        linha_atual += 1

    # salva tokens da ultima execução valida
    if tokensUltimaExecucao:
        salvarTokens(tokensUltimaExecucao)

    # gera assembly se houver expressões validas
    if linhas_tokens:

        codigoAssembly = gerarAssembly(linhas_tokens)

        if codigoAssembly:
            salvarAssembly(codigoAssembly)

    exibirResultados(resultados)

if __name__ == "__main__":
    main()