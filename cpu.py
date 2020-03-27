import sys

LDI = 0b10000010
CMP = 0b10100111
JEQ = 0b01010101
JNE = 0b01010110
JMP = 0b01010100
PRN = 0b01000111
HLT = 0b00000001


class CPU:
    def __init__(self):
        self.running = True
        self.ram = [0]*256
        self.reg = [0]*8
        self.reg[7] = 0xF4  # 11110100 or 244
        self.PC = 0
        self.FL = 0
        self.IR = None
        self.E = 0
        self.L = 0
        self.G = 0

        self.branch = {}
        self.branch[LDI] = lambda mar, mdr: self.ldi(mar, mdr)
        self.branch[CMP] = lambda mar, mdr: self.alu("CMP", mar, mdr)
        self.branch[JEQ] = lambda mar, __: self.jeq(mar)
        self.branch[JNE] = lambda mar, __: self.jne(mar)
        self.branch[JMP] = lambda mar, __: self.jmp(mar)
        self.branch[PRN] = lambda mar, __: self.prn(mar)
        self.branch[HLT] = lambda _, __: self.hlt()

        self.alu_branch = {}
        self.alu_branch["CMP"] = lambda mara, marb: self.alu_cmp(mara, marb)
        self.alu_branch["AND"] = lambda mara, marb: self.alu_and(mara, marb)
        self.alu_branch["OR"] = lambda mara, marb: self.alu_or(mara, marb)
        self.alu_branch["XOR"] = lambda mara, marb: self.alu_xor(mara, marb)
        self.alu_branch["NOT"] = lambda mar, __: self.alu_not(mar)
        self.alu_branch["SHL"] = lambda mara, marb: self.alu_shl(mara, marb)
        self.alu_branch["SHR"] = lambda mara, marb: self.alu_shr(mara, marb)
        self.alu_branch["MOD"] = lambda mara, marb: self.alu_mod(mara, marb)

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def load(self, file=None):
        address = 0
        # for line in file:
        #     comment_split = line.split("#")
        #     num = comment_split[0].strip()
        #     if num == '':
        #         continue
        #     value = int(num, 2)
        #     self.ram[address] = value
        #     address += 1
        filex = [
            0b10000010,  # LDI R0,10
            0b00000000,
            0b00001010,
            0b10000010,  # LDI R1,20
            0b00000001,
            0b00010100,
            0b10000010,  # LDI R2,TEST1
            0b00000010,
            0b00010011,
            0b10100111,  # CMP R0,R1
            0b00000000,
            0b00000001,
            0b01010101,  # JEQ R2
            0b00000010,
            0b10000010,  # LDI R3,1
            0b00000011,
            0b00000001,
            0b01000111,  # PRN R3
            0b00000011,
            # TEST1 (address 19):
            0b10000010,  # LDI R2,TEST2
            0b00000010,
            0b00100000,
            0b10100111,  # CMP R0,R1
            0b00000000,
            0b00000001,
            0b01010110,  # JNE R2
            0b00000010,
            0b10000010,  # LDI R3,2
            0b00000011,
            0b00000010,
            0b01000111,  # PRN R3
            0b00000011,
            # TEST2 (address 32):
            0b10000010,  # LDI R1,10
            0b00000001,
            0b00001010,
            0b10000010,  # LDI R2,TEST3
            0b00000010,
            0b00110000,
            0b10100111,  # CMP R0,R1
            0b00000000,
            0b00000001,
            0b01010101,  # JEQ R2
            0b00000010,
            0b10000010,  # LDI R3,3
            0b00000011,
            0b00000011,
            0b01000111,  # PRN R3
            0b00000011,
            # TEST3 (address 48):
            0b10000010,  # LDI R2,TEST4
            0b00000010,
            0b00111101,
            0b10100111,  # CMP R0,R1
            0b00000000,
            0b00000001,
            0b01010110,  # JNE R2
            0b00000010,
            0b10000010,  # LDI R3,4
            0b00000011,
            0b00000100,
            0b01000111,  # PRN R3
            0b00000011,
            # TEST4 (address 61):
            0b10000010,  # LDI R3,5
            0b00000011,
            0b00000101,
            0b01000111,  # PRN R3
            0b00000011,
            0b10000010,  # LDI R2,TEST5
            0b00000010,
            0b01001001,
            0b01010100,  # JMP R2
            0b00000010,
            0b01000111,  # PRN R3
            0b00000011,
            # TEST5 (address 73):
            0b00000001,  # HLT
        ]
        for line in filex:
            self.ram[address] = line
            address += 1

    def alu(self, op, reg_a, reg_b):
      # - [ ] Add the ALU operations: `AND` `OR` `XOR` `NOT` `SHL` `SHR` `MOD`
        if op in self.alu_branch:
            self.alu_branch[op](reg_a, reg_b)
        else:
            raise Exception("Unsupported ALU branch")

    def run(self):
        while self.running:
            self.IR = self.ram_read(self.PC)
            operand_a = self.ram_read(self.PC + 1)
            operand_b = self.ram_read(self.PC + 2)
            self.branch[self.IR](operand_a, operand_b)
            self.PC += (self.IR >> 6) + 1

    def ldi(self, mar, mdr):
        self.reg[mar] = mdr

    def hlt(self):
        self.running = False
        sys.exit()

    def prn(self, mar):
        print(self.reg[mar])

    def jmp(self, mar):
        # Jump to the address stored in the given register.
        # Set the `PC` to the address stored in the given register.
        self.PC = self.reg[mar] - 2

    def jne(self, mar):
        # If `E` flag is clear (false, 0), jump to the address stored in the given
        # register.
        if self.E is False or self.E is 0:
            self.jmp(mar)

    def jeq(self, mar):
        # If `equal` flag is set (true), jump to the address stored in the given register.
        if self.E is True or self.E is 1:
            self.jmp(mar)

    def alu_cmp(self, reg_a, reg_b):
        a_value = self.reg[reg_a]
        b_value = self.reg[reg_b]
        self.E = int(a_value == b_value)
        self.L = int(a_value < b_value)
        self.G = int(a_value > b_value)

    def alu_and(self, reg_a, reg_b):
        self.reg[reg_a] = self.reg[reg_a] & self.reg[reg_b]

    def alu_xor(self, reg_a, reg_b):
        self.reg[reg_a] = self.reg[reg_a] ^ self.reg[reg_b]

    def alu_or(self, reg_a, reg_b):
        self.reg[reg_a] = self.reg[reg_a] | self.reg[reg_b]

    def alu_shl(self, reg_a, reg_b):
        self.reg[reg_a] = self.reg[reg_a] << self.reg[reg_b]

    def alu_shr(self, reg_a, reg_b):
        self.reg[reg_a] = self.reg[reg_a] >> self.reg[reg_b]

    def alu_mod(self, reg_a, reg_b):
        self.reg[reg_a] = self.reg[reg_a] % self.reg[reg_b]

    def alu_not(self, reg_a):
        self.reg[reg_a] = ~self.reg[reg_a]


# - [ ] Add the ALU operations: `AND` `OR` `XOR` `NOT` `SHL` `SHR` `MOD`
# - [ ] Add an `ADDI` extension instruction to add an immediate value to a register
# - [ ] Add timer interrupts
# - [ ] Add keyboard interrupts