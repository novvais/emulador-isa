# Explicacao do projeto

O projeto simula uma ISA didatica pequena. A ideia foi montar uma maquina simples, mas com as partes principais que aparecem no enunciado: contador de programa (`PC`), registradores (`R0` ate `R4`), memoria de dados com 32 posicoes e memoria de instrucoes.

Durante a execucao, o `PC` indica qual instrucao deve ser buscada. Depois disso, o parser separa a operacao e os operandos, e o core faz a parte de executar a instrucao. Quando precisa, ele altera registradores ou memoria e depois atualiza o `PC`.

## Papel dos arquivos

- `hardware.py`: guarda o estado da maquina.
- `parser.py`: transforma texto assembly em dicionarios usados pelo emulador.
- `core.py`: executa `LOAD`, `STORE`, `ADD`, `SUB` e `HALT`.
- `main.py`: junta as partes e mostra o passo a passo no terminal.
- `testar_programas.py`: roda os programas usados na entrega e confere a memoria final.

## Testes usados

O teste obrigatorio usa `Mem[10] = 7` e `Mem[11] = 5`. No final, precisa deixar `Mem[12] = 12` e `Mem[13] = 5`.

O teste extra usa `Mem[20] = 15` e `Mem[21] = 4`. No final, precisa deixar `Mem[22] = 11` e `Mem[23] = 15`.

Com esses dois testes da para mostrar que o acesso a memoria funciona com `LOAD` e `STORE`, e que as contas entre registradores funcionam com `ADD` e `SUB`.
