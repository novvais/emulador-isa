# Emulador de uma ISA didatica

Este projeto e um emulador pequeno de uma ISA didatica, feito para mostrar na pratica como uma maquina simples busca, interpreta e executa instrucoes. O programa le instrucoes em um formato parecido com assembly, guarda essas instrucoes na memoria do emulador e mostra o estado da maquina durante a execucao.

## Estrutura principal

- `main.py`: carrega e executa um programa `.asm`.
- `src/hardware.py`: define PC, registradores, memoria de dados e memoria de instrucoes.
- `src/parser.py`: le e decodifica as instrucoes.
- `src/core.py`: executa cada instrucao.
- `programs/required_test.asm`: programa de teste obrigatorio.
- `programs/extra_test.asm`: segundo programa de teste.
- `testar_programas.py`: roda os testes da entrega e confere se a memoria final ficou correta.
- `teste_core.py`: demonstracao menor do core, usada para acompanhar o teste obrigatorio passo a passo.

## Instrucoes implementadas

- `LOAD Rd, offset(Rs1)`: carrega da memoria para um registrador.
- `STORE Rs2, offset(Rs1)`: salva o valor de um registrador na memoria.
- `ADD Rd, Rs1, Rs2`: soma dois registradores.
- `SUB Rd, Rs1, Rs2`: subtrai dois registradores.
- `HALT`: encerra a execucao.

Tambem existem as instrucoes opcionais `JMP` e `BEQ` no codigo.

## Como executar

Para rodar o teste obrigatorio:

```bash
python main.py
```

Para escolher outro programa:

```bash
python main.py programs/extra_test.asm
```

Para verificar os dois programas de teste de uma vez:

```bash
python testar_programas.py
```

O `teste_core.py` ficou no projeto como uma demonstracao separada da parte de execucao. Ele ajuda a ver o teste obrigatorio andando passo a passo, mas para conferir a entrega completa o melhor caminho e usar `main.py` e `testar_programas.py`.

## Teste obrigatorio

Programa:

```asm
LOAD R1, 10(R0)
LOAD R2, 11(R0)
ADD R3, R1, R2
SUB R4, R3, R1
STORE R3, 12(R0)
STORE R4, 13(R0)
HALT
```

Memoria inicial:

- `Mem[10] = 7`
- `Mem[11] = 5`

Resultado esperado:

- `Mem[12] = 12`
- `Mem[13] = 5`

## Teste extra

Programa:

```asm
LOAD R1, 20(R0)
LOAD R2, 21(R0)
SUB R3, R1, R2
ADD R4, R3, R2
STORE R3, 22(R0)
STORE R4, 23(R0)
HALT
```

Memoria inicial:

- `Mem[20] = 15`
- `Mem[21] = 4`

Resultado esperado:

- `Mem[22] = 11`
- `Mem[23] = 15`

## Saida no terminal

Durante a execucao, o emulador mostra:

- valor atual do `PC`;
- instrucao executada;
- registradores `R0` ate `R4`;
- posicoes da memoria alteradas por `STORE`;
- comparacao final com o resultado esperado nos programas de teste.
