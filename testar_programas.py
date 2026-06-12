# testar_programas.py
# Conferência final dos programas usados na entrega.
# A ideia aqui não é mostrar cada passo, e sim rodar tudo e ver se a memória
# terminou com os valores que o enunciado pede.

# Como rodar:
#   python testar_programas.py

from src.hardware import Hardware
from src.parser import carregar_arquivo_asm
from src.core import executar_instrucao


# Casos de teste que vamos conferir no final.
TESTES = [
    {
        "nome": "Teste obrigatorio",
        "arquivo": "programs/required_test.asm",
        "memoria_inicial": {10: 7, 11: 5},
        "esperado": {12: 12, 13: 5},
    },
    {
        "nome": "Teste extra",
        "arquivo": "programs/extra_test.asm",
        "memoria_inicial": {20: 15, 21: 4},
        "esperado": {22: 11, 23: 15},
    },
]


def rodar_programa(arquivo, memoria_inicial):
    # Cada programa roda em um hardware limpo.
    hw = Hardware()
    hw.load_program(carregar_arquivo_asm(arquivo))

    # Coloca na memoria os valores que seriam os dados de entrada.
    for endereco, valor in memoria_inicial.items():
        hw.memory[endereco] = valor

    # Para quando a instrucao HALT for executada.
    while True:
        instrucao = hw.instructions[hw.pc]
        resultado = executar_instrucao(hw, instrucao)
        if not resultado["continua"]:
            break

    return hw


def main():
    # Comeca assumindo que tá tudo certo, e muda se algum resultado não bater.
    passou_tudo = True

    for teste in TESTES:
        hw = rodar_programa(teste["arquivo"], teste["memoria_inicial"])
        print(teste["nome"])

        # Não precisa imprimir a memória inteira, só as posições que o teste usa.
        for endereco, esperado in teste["esperado"].items():
            obtido = hw.memory[endereco]
            passou = obtido == esperado
            passou_tudo = passou_tudo and passou
            status = "OK" if passou else "FALHOU"
            print(f"  Mem[{endereco}] = {obtido} | esperado {esperado} | {status}")

        print()

    if passou_tudo:
        print("Todos os testes passaram.")
    else:
        print("Algum teste falhou.")
        raise SystemExit(1)


if __name__ == "__main__":
    main()