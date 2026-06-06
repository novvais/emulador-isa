class ErroDeSintaxe(Exception):
    pass
# (R3 -> 3)
def ler_registrador(texto):
    texto = texto.strip().upper()
    if not texto.startswith("R"):
        raise ErroDeSintaxe(f"Esperava um registrador (ex: R1), mas veio '{texto}'")
    try:
        return int(texto[1:])
    except ValueError:
        raise ErroDeSintaxe(f"Registrador invalido: '{texto}'")
#10(R0) -> (10, 0)
def ler_offset_e_base(texto):
    texto = texto.strip()
    if "(" not in texto or not texto.endswith(")"):
        raise ErroDeSintaxe(f"Esperava o formato offset(Rx), mas veio '{texto}'")
    parte_offset, parte_registrador = texto.split("(", 1)
    parte_registrador = parte_registrador[:-1]
    try:
        offset = int(parte_offset.strip())
    except ValueError:
        raise ErroDeSintaxe(f"Offset invalido: '{parte_offset}'")
    return offset, ler_registrador(parte_registrador)
def decodificar_linha(linha):
    linha = linha.split("#")[0].strip()
    if linha == "":
        return None
    pedacos = linha.split(None, 1)
    nome = pedacos[0].upper()
    resto = pedacos[1] if len(pedacos) > 1 else ""
    operandos = [item.strip() for item in resto.split(",") if item.strip() != ""]
    if nome == "LOAD":
        if len(operandos) != 2:
            raise ErroDeSintaxe("LOAD precisa de 2 operandos: LOAD rd, offset(rs1)")
        rd = ler_registrador(operandos[0])
        offset, rs1 = ler_offset_e_base(operandos[1])
        return {"op": "LOAD", "rd": rd, "offset": offset, "rs1": rs1}
    elif nome == "STORE":
        if len(operandos) != 2:
            raise ErroDeSintaxe("STORE precisa de 2 operandos: STORE rs2, offset(rs1)")
        rs2 = ler_registrador(operandos[0])
        offset, rs1 = ler_offset_e_base(operandos[1])
        return {"op": "STORE", "rs2": rs2, "offset": offset, "rs1": rs1}
    elif nome == "ADD" or nome == "SUB":
        if len(operandos) != 3:
            raise ErroDeSintaxe(f"{nome} precisa de 3 operandos: {nome} rd, rs1, rs2")
        rd = ler_registrador(operandos[0])
        rs1 = ler_registrador(operandos[1])
        rs2 = ler_registrador(operandos[2])
        return {"op": nome, "rd": rd, "rs1": rs1, "rs2": rs2}
    elif nome == "HALT":
        return {"op": "HALT"}
    # FUNCIONALIDADE OPCIONAL: leitura dos desvios JMP e BEQ 
    elif nome == "JMP":
        if len(operandos) != 1:
            raise ErroDeSintaxe("JMP precisa de 1 operando: JMP destino")
        try:
            destino = int(operandos[0])
        except ValueError:
            raise ErroDeSintaxe(f"Destino do JMP invalido: '{operandos[0]}'")
        return {"op": "JMP", "destino": destino}
    elif nome == "BEQ":
        if len(operandos) != 3:
            raise ErroDeSintaxe("BEQ precisa de 3 operandos: BEQ rs1, rs2, destino")
        rs1 = ler_registrador(operandos[0])
        rs2 = ler_registrador(operandos[1])
        try:
            destino = int(operandos[2])
        except ValueError:
            raise ErroDeSintaxe(f"Destino do BEQ invalido: '{operandos[2]}'")
        return {"op": "BEQ", "rs1": rs1, "rs2": rs2, "destino": destino}
    else:
        raise ErroDeSintaxe(f"Instrucao desconhecida: '{nome}'")
def decodificar_programa(linhas):
    programa = []
    for numero_da_linha, linha in enumerate(linhas, start=1):
        try:
            ficha = decodificar_linha(linha)
        except ErroDeSintaxe as erro:
            raise ErroDeSintaxe(f"Erro na linha {numero_da_linha}: {erro}")
        if ficha is not None:
            programa.append(ficha)
    return programa
#FUNCIONALIDADE OPCIONAL: carregar o programa a partir de um arquivo .asm;
def carregar_arquivo_asm(caminho):
    with open(caminho, "r", encoding="utf-8") as arquivo:
        linhas = arquivo.readlines()
    return decodificar_programa(linhas)