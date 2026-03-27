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

def extrair_variaveis(tokens_por_linha):

    variaveis = set()

    for tokens in tokens_por_linha:
        for token in tokens:
            if isVariavel(token): 
                variaveis.add(token)

    return variaveis

def construir_pool_constantes(tokens_por_linha):

    constantes = {"0.0": "const_zero", "1.0": "const_one"}
    
    for tokens in tokens_por_linha:
        for token in tokens:

            if isNumero(token):

                val_f = float(token)

                # Verifica se a constante já existe no pool
                existe = False
                for k in constantes.keys():
                    if float(k) == val_f:
                        existe = True
                        break

                if not existe:
                    label = f"const_{len(constantes)}"
                    constantes[str(val_f)] = label
                    
    return constantes


def get_label_constante(token, constantes):

    val_f = float(token)

    for k, v in constantes.items():
        if float(k) == val_f: 
            return v

    return None

def gerar_data_section(variaveis, constantes):

    asm = []

    asm.append(".data")
    asm.append("    .align 3")

    asm.append("RES: .space 8000")

    asm.append("RES_size: .word 0")

    asm.append("    .align 2")
    asm.append("display_lut: .word 0x3F, 0x06, 0x5B, 0x4F, 0x66, 0x6D, 0x7D, 0x07, 0x7F, 0x6F, 0x77, 0x7C, 0x39, 0x5E, 0x79, 0x71")
    
    asm.append("    .align 3")  
    
    # Inserção das constantes no pool
    for k, v in constantes.items():
        asm.append(f"    {v}: .double {k}")

    for var in variaveis:
        asm.append(f"    var_{var}: .double 0.0")
        
    return asm


def gerar_comando_res():

    asm = []

    asm.append("    VPOP {D0}")
    asm.append("    VCVT.S32.F64 S0, D0")
    asm.append("    VMOV R1, S0")

    # Verifica se o índice é negativo
    asm.append("    CMP R1, #0")
    asm.append("    BLT throw_error")

    # Carrega tamanho atual do array
    asm.append("    LDR R2, =RES_size")
    asm.append("    LDR R2, [R2]")

    # Verifica se indice é maior que tamanho
    asm.append("    CMP R1, R2")
    asm.append("    BGE throw_error")

    # Ajuste para acessar posição correta
    asm.append("    SUB R1, R2, R1")
    asm.append("    SUB R1, R1, #1")

    asm.append("    LDR R0, =RES")
    asm.append("    ADD R0, R0, R1, LSL #3")

    asm.append("    VLDR.F64 D0, [R0]")
    asm.append("    VPUSH {D0}")

    return asm


def gerar_operacao_matematica(token, op_id):

    asm = []

    # Remove operandos da pilha
    asm.append("    VPOP {D1}")
    asm.append("    VPOP {D0}")

    if token == "+":
        asm.append("    VADD.F64 D0, D0, D1")
        
    elif token == "-":
        asm.append("    VSUB.F64 D0, D0, D1")
        
    elif token == "*":
        asm.append("    VMUL.F64 D0, D0, D1")
        
    elif token == "/":

        # Proteção contra divisão por zero
        asm.append("    LDR R4, =const_zero")
        asm.append("    VLDR.F64 D2, [R4]")
        asm.append("    VCMP.F64 D1, D2")
        asm.append("    VMRS APSR_nzcv, FPSCR")
        asm.append("    BEQ throw_error")

        asm.append("    VDIV.F64 D0, D0, D1")
        
    elif token == "//":

        asm.append("    LDR R4, =const_zero")
        asm.append("    VLDR.F64 D2, [R4]")
        asm.append("    VCMP.F64 D1, D2")
        asm.append("    VMRS APSR_nzcv, FPSCR")
        asm.append("    BEQ throw_error")

        asm.append("    VDIV.F64 D0, D0, D1")
        asm.append("    VCVT.S32.F64 S0, D0")
        asm.append("    VCVT.F64.S32 D0, S0")
        
    elif token == "%":

        asm.append("    LDR R4, =const_zero")
        asm.append("    VLDR.F64 D2, [R4]")
        asm.append("    VCMP.F64 D1, D2")
        asm.append("    VMRS APSR_nzcv, FPSCR")
        asm.append("    BEQ throw_error")

        asm.append("    VDIV.F64 D2, D0, D1")
        asm.append("    VCVT.S32.F64 S4, D2")
        asm.append("    VCVT.F64.S32 D2, S4")
        asm.append("    VMUL.F64 D2, D2, D1")
        asm.append("    VSUB.F64 D0, D0, D2")
        
    elif token == "^":

        asm.append("    VCVT.S32.F64 S2, D1")
        asm.append("    VMOV R3, S2")

        asm.append("    CMP R3, #0")
        asm.append("    BLT throw_error")

        asm.append("    LDR R4, =const_one")
        asm.append("    VLDR.F64 D2, [R4]")
        
        asm.append(f"pow_loop_{op_id}:")
        asm.append("    CMP R3, #0")
        asm.append(f"    BEQ pow_end_{op_id}")
        asm.append("    VMUL.F64 D2, D2, D0")
        asm.append("    SUB R3, R3, #1")
        asm.append(f"    B pow_loop_{op_id}")
        
        asm.append(f"pow_end_{op_id}:")
        asm.append("    VMOV.F64 D0, D2")

    asm.append("    VPUSH {D0}")

    return asm

def gerar_salvamento_linha(line_id):

    asm = []

    asm.append("    VPOP {D0}")

    asm.append(f"save_res_step_{line_id}:")

    asm.append("    LDR R0, =RES_size")
    asm.append("    LDR R1, [R0]")

    # Evita overflow do array
    asm.append("    CMP R1, #1000")
    asm.append("    BGE throw_error")

    asm.append("    LDR R2, =RES")
    asm.append("    ADD R2, R2, R1, LSL #3") 

    asm.append("    VSTR.F64 D0, [R2]")

    asm.append("    ADD R1, R1, #1")
    asm.append("    STR R1, [R0]")

    return asm

def gerar_text_section(tokens_por_linha, constantes):

    asm = []

    asm.append("\n.text")
    asm.append(".global _start")
    asm.append("_start:")

    line_id = 0
    op_id = 0

    for tokens in tokens_por_linha:
 
        # Caso linha tenha erro (tokens vazios)
        if not tokens:
            asm.append("    LDR R0, =const_zero")
            asm.append("    VLDR.F64 D0, [R0]")
            asm.append("    VPUSH {D0}")
            
        for i, token in enumerate(tokens):

            if token in ("(", ")"):
                continue

            if isNumero(token):

                label = get_label_constante(token, constantes)

                asm.append(f"    LDR R0, ={label}")
                asm.append("    VLDR.F64 D0, [R0]")
                asm.append("    VPUSH {D0}")

                continue

            if isVariavel(token):

                # Leitura de variavel
                if i > 0 and tokens[i - 1] == "(" and i + 1 < len(tokens) and tokens[i + 1] == ")":

                    asm.append(f"    LDR R0, =var_{token}")
                    asm.append("    VLDR.F64 D0, [R0]")
                    asm.append("    VPUSH {D0}")

                # Escrita em variavel
                else:

                    asm.append("    VPOP {D0}")
                    asm.append(f"    LDR R0, =var_{token}")
                    asm.append("    VSTR.F64 D0, [R0]")
                    asm.append("    VPUSH {D0}")

                continue

            if token == "RES":

                asm.extend(gerar_comando_res())
                continue

            if token in OPERADORES:

                asm.extend(gerar_operacao_matematica(token, op_id))

                if token == "^":
                    op_id += 1 

                continue

        asm.extend(gerar_salvamento_linha(line_id))
        line_id += 1

    return asm

def gerar_finalizacao():

    asm = []

    asm.append("    VCVT.S32.F64 S0, D0")     
    asm.append("    VMOV R1, S0")             
    
    asm.append("    LDR R2, =0xFF200020")     
    asm.append("    LDR R3, =display_lut")    
    asm.append("    MOV R4, #0")              
    
    # Conversão para cada digito hexadecimal

    asm.append("    AND R6, R1, #0xF")        
    asm.append("    LDR R7, [R3, R6, LSL #2]")
    asm.append("    ORR R4, R4, R7")        

    asm.append("    LSR R1, R1, #4")         
    asm.append("    AND R6, R1, #0xF")
    asm.append("    LDR R7, [R3, R6, LSL #2]")
    asm.append("    LSL R7, R7, #8")         
    asm.append("    ORR R4, R4, R7")

    asm.append("    LSR R1, R1, #4")          
    asm.append("    AND R6, R1, #0xF")
    asm.append("    LDR R7, [R3, R6, LSL #2]")
    asm.append("    LSL R7, R7, #16")         
    asm.append("    ORR R4, R4, R7")

    asm.append("    LSR R1, R1, #4")          
    asm.append("    AND R6, R1, #0xF")
    asm.append("    LDR R7, [R3, R6, LSL #2]")
    asm.append("    LSL R7, R7, #24")         
    asm.append("    ORR R4, R4, R7")

    asm.append("    STR R4, [R2]")            

    asm.append("    B fim")

    # Tratamento de erro
    asm.append("throw_error:")
    asm.append("    LDR R0, =0xFF200000")     
    asm.append("    LDR R1, =0x3FF")        
    asm.append("    STR R1, [R0]")
    asm.append("    B .")
    
    asm.append("fim:")
    asm.append("    NOP")
    asm.append("    B .")
    
    return asm

def gerarAssembly(tokens_por_linha):

    variaveis = extrair_variaveis(tokens_por_linha)
    constantes = construir_pool_constantes(tokens_por_linha)

    asm = []

    asm.extend(gerar_data_section(variaveis, constantes))
    asm.extend(gerar_text_section(tokens_por_linha, constantes))
    asm.extend(gerar_finalizacao())
    
    return "\n".join(asm)


def salvarAssembly(codigo, nome_arquivo="program.s"):

    with open(nome_arquivo, "w", encoding="utf-8") as f:
        f.write(codigo)


OPERADORES = {"+", "-", "*", "/", "//", "%", "^"}


def isNumero(token):

    try: 
        float(token)
        return True
    except ValueError: 
        return False


def isVariavel(token):

    return token.isalpha() and token.isupper() and token != "RES"