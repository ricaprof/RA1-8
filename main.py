import sys
import json

from lexer import parseExpressao
from executor import executarExpressao
from assembly import gerarAssembly, salvarAssembly


def salvar_tokens(tokens_por_linha, nome_arquivo="tokens.txt"):

    with open(nome_arquivo, "w", encoding="utf-8") as f:
        json.dump(tokens_por_linha, f, indent=4, ensure_ascii=False)

def processar_arquivo(nome_arquivo):

    historico_resultados = []   
    tokens_por_linha = []       
    memoria_local = {}         

    try:
        with open(nome_arquivo, "r", encoding="utf-8") as f:
            linhas = f.readlines()
    except FileNotFoundError:
        print(f"Erro: O arquivo '{nome_arquivo}' não foi encontrado.")
        sys.exit(1)

    print(f"\n=== PROCESSANDO ARQUIVO: {nome_arquivo} ===\n")

    # Percorre todas as linhas do arquivo
    for numero_linha, linha in enumerate(linhas, start=1):

        linha = linha.strip()

        # Ignora linhas completamente vazias
        if not linha:
            continue

        print(f"Linha {numero_linha}: {linha}")

        try:

            tokens = parseExpressao(linha)

            # Usa o executor passando o historico e a memoria atual
            resultado = executarExpressao(tokens, historico_resultados, memoria_local)

            # Guarda o resultado no historico
            historico_resultados.append(resultado)

            # Guarda os tokens gerados
            tokens_por_linha.append(tokens)

            print(f"  Tokens: {tokens}")
            print(f"  Resultado: {resultado:.2f}\n")

        except Exception as e:
            # Caso ocorra erro na linha registramos o erro
            print(f" Erro: {e}\n")

            historico_resultados.append(0.0)

            tokens_por_linha.append([])

    # Salva os tokens em formato estruturado
    salvar_tokens(tokens_por_linha)
    print("Tokens estruturados salvos em 'tokens.txt'")


    if tokens_por_linha:
        try:
            codigo_assembly = gerarAssembly(tokens_por_linha)
            salvarAssembly(codigo_assembly)

            print("Assembly gerado com sucesso em 'program.s'")

        except Exception as e:
            print(f"Erro ao gerar o Assembly: {e}")
    else:
        print("Nenhum token para gerar Assembly.")

    print("\n=== FIM DA EXECUÇÃO ===")

def main():

    if len(sys.argv) < 2:
        print("Uso correto: python main.py <nome_do_arquivo.txt>")
        sys.exit(1)

    # Nome do arquivo passado pelo usuário
    nome_arquivo = sys.argv[1]

    processar_arquivo(nome_arquivo)

if __name__ == "__main__":
    main()