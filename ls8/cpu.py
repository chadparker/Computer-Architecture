"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.reg[7] = 0xF4
        self.pc = 0
        self.ir = 0
        self.mar = 0
        self.mdr = 0
        self.fl = 0
        self.halted = False

    def load(self, filename):
        """Load a program into memory."""

        address = 0
        program = []

        with open(filename) as f:
            for line in f:
                comment_split = line.split("#")
                maybe_binary_number = comment_split[0]

                try:
                    x = int(maybe_binary_number, 2)
                    program.append(x)
                except:
                    continue

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == MUL:
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        while not self.halted:
            # IR (Instruction Register) = value at memory address in PC (Program Counter)
            ir = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            self.execute_instruction(ir, operand_a, operand_b)

    def execute_instruction(self, instruction, operand_a, operand_b):
        if instruction == HLT:
            self.halted = True
            self.pc += self.number_of_operands(instruction)
        elif instruction == PRN:
            print(self.reg[operand_a])
            self.pc += self.number_of_operands(instruction)
        elif instruction == LDI:
            self.reg[operand_a] = operand_b
            self.pc += self.number_of_operands(instruction)
        elif instruction == MUL:
            self.alu(instruction, operand_a, operand_b)
            self.pc += self.number_of_operands(instruction)
        else:
            print("INVALID INSTRUCTION.")
    
    def number_of_operands(self, instruction):
        # Instruction layout: 'AABCDDDD'
        # * AA = Number of operands for this opcode, 0-2
        # INSTRUCTION = 0b10000010 # >> 6 --> 0b10 & 0b11 --> 0b10
        return ((instruction >> 6) & 0b11) + 1

    def ram_read(self, MAR): # Memory Address Register
        return self.ram[MAR]
    
    def ram_write(self, MDR, MAR): # Memory Data Register, Memory Address Register
        self.ram[MAR] = MDR
