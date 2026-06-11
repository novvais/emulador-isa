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
}


def main():
    caminho = sys.argv[1] if len(sys.argv) > 1 else "programs/required_test.asm"

    programa = carregar_arquivo_asm(caminho)

    hw = Hardware()
    hw.load_program(programa)

    nome_arquivo = os.path.basename(caminho)
    for endereco, valor in DADOS_INICIAIS.get(nome_arquivo, {}).items():
        hw.memory[endereco] = valor

    print(f"Programa carregado: {caminho} ({len(hw.instructions)} instrucoes)")
    print()

    while True:
        instrucao = hw.instructions[hw.pc]
        print(f"PC={hw.pc} -> {instrucao}")
        resultado = executar_instrucao(hw, instrucao)
        hw.show_state(resultado["memoria_alterada"])
        if not resultado["continua"]:
            print("HALT - execucao encerrada")
            break


if __name__ == "__main__":
    main()
