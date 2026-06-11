# teste_core.py
# Script de demonstracao da Funcao 3 (core.py)
# Roda o programa de teste obrigatorio passo a passo, mostrando
# PC, registradores e memoria apos cada instrucao.
#
# Como rodar:
#   python3 teste_core.py

from src.hardware import Hardware
from src.parser import decodificar_programa
from src.core import executar_instrucao

programa_texto = [
    "LOAD R1, 10(R0)",
    "LOAD R2, 11(R0)",
    "ADD R3, R1, R2",
    "SUB R4, R3, R1",
    "STORE R3, 12(R0)",
    "STORE R4, 13(R0)",
    "HALT",
]

programa = decodificar_programa(programa_texto)

hw = Hardware()
hw.memory[10] = 7
hw.memory[11] = 5

passo = 1
while True:
    instrucao = programa[hw.pc]
    print(f"=== Passo {passo}: PC={hw.pc} -> {instrucao} ===")
    resultado = executar_instrucao(hw, instrucao)
    hw.show_state(resultado["memoria_alterada"])
    if not resultado["continua"]:
        print("HALT - execucao encerrada")
        break
    passo += 1

print("Mem[12] =", hw.memory[12], "(esperado 12)")
print("Mem[13] =", hw.memory[13], "(esperado 5)")
