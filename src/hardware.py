# hardware.py — Função 1
# Define a estrutura do hardware: PC, registradores e memória de dados

NUM_REGISTERS = 5   # R0 até R4
MEMORY_SIZE   = 32  # 32 posições de memória

class Hardware:
    def __init__(self):
        # PC começa em 0 — aponta para a primeira instrução
        self.pc = 0

        # 5 registradores (R0 a R4), todos começando com 0
        self.registers = [0] * NUM_REGISTERS

        # 32 posições de memória de dados, todas começando com 0
        self.memory = [0] * MEMORY_SIZE

    def read_register(self, index):
        # R0 é sempre zero (regra da arquitetura, igual ao RISC-V)
        if index == 0:
            return 0
        return self.registers[index]

    def write_register(self, index, value):
        # Escrever em R0 não faz nada — ele é fixo em zero
        if index == 0:
            return
        self.registers[index] = value

    def read_memory(self, address):
        return self.memory[address]

    def write_memory(self, address, value):
        self.memory[address] = value

    def advance_pc(self):
        # Avança para a próxima instrução
        self.pc += 1

    def show_state(self, memory_changes=None):
        # Exibe PC, registradores e alterações na memória
        print(f"  PC: {self.pc}")
        regs = " | ".join(f"R{i}={self.registers[i]}" for i in range(NUM_REGISTERS))
        print(f"  Registradores: {regs}")
        if memory_changes:
            for addr in memory_changes:
                print(f"  Mem[{addr}] = {self.memory[addr]}")
        print()
        