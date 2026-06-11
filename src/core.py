# core.py — Função 3
# Executa o comportamento real de cada instrução já decodificada pelo parser

def executar_instrucao(hardware, instrucao):
    """
    Recebe o hardware (PC, registradores, memória) e uma instrução já
    decodificada (dict vindo do parser, ex: {"op": "ADD", "rd": 3, "rs1": 1, "rs2": 2}).

    Executa a instrução, atualiza registradores/memória/PC e devolve um
    dict com informações para exibição:
      - "continua": False quando a instrução for HALT, True caso contrário
      - "memoria_alterada": lista de endereços de memória que mudaram
    """
    op = instrucao["op"]
    memoria_alterada = []
    continua = True
    pc_alterado = False

    if op == "LOAD":
        endereco = hardware.read_register(instrucao["rs1"]) + instrucao["offset"]
        valor = hardware.read_memory(endereco)
        hardware.write_register(instrucao["rd"], valor)

    elif op == "STORE":
        endereco = hardware.read_register(instrucao["rs1"]) + instrucao["offset"]
        valor = hardware.read_register(instrucao["rs2"])
        hardware.write_memory(endereco, valor)
        memoria_alterada.append(endereco)

    elif op == "ADD":
        resultado = hardware.read_register(instrucao["rs1"]) + hardware.read_register(instrucao["rs2"])
        hardware.write_register(instrucao["rd"], resultado)

    elif op == "SUB":
        resultado = hardware.read_register(instrucao["rs1"]) - hardware.read_register(instrucao["rs2"])
        hardware.write_register(instrucao["rd"], resultado)

    elif op == "HALT":
        continua = False

    # FUNCIONALIDADE OPCIONAL: instruções de desvio JMP e BEQ
    elif op == "JMP":
        hardware.pc = instrucao["destino"]
        pc_alterado = True

    elif op == "BEQ":
        if hardware.read_register(instrucao["rs1"]) == hardware.read_register(instrucao["rs2"]):
            hardware.pc = instrucao["destino"]
            pc_alterado = True

    else:
        raise ValueError(f"Instrucao desconhecida: '{op}'")

    # Avança o PC para a próxima instrução, exceto quando HALT encerra
    # a execução ou quando um desvio (JMP/BEQ) já definiu o novo PC
    if op != "HALT" and not pc_alterado:
        hardware.advance_pc()

    return {"continua": continua, "memoria_alterada": memoria_alterada}
