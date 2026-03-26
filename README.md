# Gerador de Assembly ARMv7 (CPULATOR) com suporte a IEEE754 64 bits

## Instituição
PUCPR - Pontifícia Universidade Católica do Paraná

## Integrantes (ordem alfabética)
- Murilo Chandelier Pedrazzani - https://github.com/MuriloPedrazzani
- Ricardo Ryu Magalhães Makino - https://github.com/ryumakino
- Ricardo Vinicius Moreira Vianna - https://github.com/ricaprof

## Grupo no Canvas
RA1 8

## Disciplina
Construção de Interpretadores

## Professor
Frank Alcantara

## Descrição
Este projeto implementa um analisador léxico e gerador de código Assembly para ARMv7 DEC1-SOC(v16.1) que processa expressões aritméticas em notação polonesa reversa (RPN). Suporta operações básicas, comandos especiais de memória e histórico, e gera código Assembly compatível com o simulador CPULATOR.

## Funcionalidades
- Analisador léxico usando máquinas de estado finito (FSM)
- Execução de expressões RPN com precisão IEEE 754 64 bits
- Geração de código Assembly ARMv7
- Suporte a operações: +, -, *, /, //, %, ^
- Comandos especiais: RES (resultado anterior), MEM (memória)
- Interfaces com simulador: LEDs para exibir resultado final

## Como Compilar e Executar
1. Certifique-se de ter o Python 3 instalado em sua máquina.
2. Execute o programa principal passando um dos arquivos de teste como argumento: 
   `python main.py teste1.txt`
3. O programa gerará a saída no terminal, além de atualizar os arquivos `program.s` (código Assembly) e `tokens.txt` (tokens processados na última execução).

## Como Testar no Simulador (CPULATOR)
1. Acesse o [CPULATOR (ARMv7 DE1-SoC)](https://cpulator.01xz.net/?sys=arm-de1soc).
2. Copie todo o conteúdo gerado dentro do arquivo `program.s`.
3. Cole no editor de código do simulador.
4. Pressione `F5` (Compile and Load) e depois `F3` (Run). O resultado final será exibido no display de LEDs da placa.

## Testes do Analisador Léxico
Execute o script de testes automatizados para validar a resiliência da Máquina de Estados contra entradas válidas e inválidas:
`python teste_lexer.py`

## Arquivos de Teste
- `teste1.txt`: 10 expressões incluindo todas as operações e comandos
- `teste2.txt`: 10 expressões incluindo todas as operações e comandos
- `teste3.txt`: 10 expressões incluindo todas as operações e comandos

## Requisitos Cumpridos
- FSM sem uso de regex
- Precisão 64 bits IEEE 754
- Arquivos de teste com mínimo 10 linhas cada
- Código Assembly funcional
- Tratamento de erros de leitura de arquivo e matemáticos (ex: divisão por zero)
- Documentação completa