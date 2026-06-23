# main.py
# Ciclo principal do emulador: busca, decodifica e executa o programa
# carregado, exibindo o estado da maquina apos cada instrucao.

import sys
import os

from src.hardware import Hardware
from src.parser import carregar_arquivo_asm
from src.core import executar_instrucao

# Valores iniciais de memoria exigidos por cada programa de teste
DADOS_INICIAIS = {
    "required_test.asm": {10: 7, 11: 5},
    "extra_test.asm": {20: 15, 21: 4},
    "branch_test.asm": {20: 15, 21: 4},
}

RESULTADOS_ESPERADOS = {
    "required_test.asm": {12: 12, 13: 5},
    "extra_test.asm": {22: 11, 23: 15},
    "branch_test.asm": {22: 11},
}

def formatar_instrucao(instrucao):
    # Mostra a instrucao parecida com assembly.
    op = instrucao["op"]

    if op == "LOAD":
        return f"LOAD R{instrucao['rd']}, {instrucao['offset']}(R{instrucao['rs1']})"
    if op == "STORE":
        return f"STORE R{instrucao['rs2']}, {instrucao['offset']}(R{instrucao['rs1']})"
    if op in ("ADD", "SUB"):
        return f"{op} R{instrucao['rd']}, R{instrucao['rs1']}, R{instrucao['rs2']}"
    if op == "JMP":
        return f"JMP {instrucao['destino']}"
    if op == "BEQ":
        return f"BEQ R{instrucao['rs1']}, R{instrucao['rs2']}, {instrucao['destino']}"
    return op

def mostrar_cabecalho(caminho, quantidade_instrucoes):
    print("=" * 64)
    print(" EMULADOR DE ISA DIDATICA")
    print("=" * 64)
    print(f"Programa carregado: {caminho}")
    print(f"Instrucoes na memoria: {quantidade_instrucoes}")
    print("-" * 64)
    print("Execucao passo a passo")
    print("-" * 64)

def main():
    caminho = sys.argv[1] if len(sys.argv) > 1 else "programs/required_test.asm"

    programa = carregar_arquivo_asm(caminho)

    hw = Hardware()
    hw.load_program(programa)

    nome_arquivo = os.path.basename(caminho)
    for endereco, valor in DADOS_INICIAIS.get(nome_arquivo, {}).items():
        hw.memory[endereco] = valor

    mostrar_cabecalho(caminho, len(hw.instructions))

    # Contador usado apenas na exibicao.
    passo = 1
    while True:
        instrucao = hw.instructions[hw.pc]
        pc_atual = hw.pc
        print(f"Passo {passo:02d} | PC={pc_atual} | {formatar_instrucao(instrucao)}")
        resultado = executar_instrucao(hw, instrucao)
        hw.show_state(resultado["memoria_alterada"])
        if not resultado["continua"]:
            print("HALT encontrado. Execucao encerrada.")
            break
        passo += 1

    esperados = RESULTADOS_ESPERADOS.get(nome_arquivo, {})
    if esperados:
        print("-" * 64)
        print("Resultado final:")
        tudo_certo = True
        for endereco, esperado in esperados.items():
            obtido = hw.memory[endereco]
            status = "OK" if obtido == esperado else "ERRO"
            print(f"  Mem[{endereco}] = {obtido} (esperado {esperado}) - {status}")
            if obtido != esperado:
                tudo_certo = False
        print("-" * 64)
        print("Teste conferido com sucesso." if tudo_certo else "Teste terminou com diferenca.")

if __name__ == "__main__":
    main()