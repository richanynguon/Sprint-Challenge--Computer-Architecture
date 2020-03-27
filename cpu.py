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

        self.branch = {}
        self.branch[LDI] = lambda mar, mdr: self.ldi(mar, mdr)
        self.branch[CMP] = lambda _, __: self.cmp()
        self.branch[JEQ] = lambda _, __: self.jeq()
        self.branch[JNE] = lambda _, __: self.jne()
        self.branch[JMP] = lambda _, __: self.jmp()
        self.branch[PRN] = lambda mar, __: self.prn(mar)
        self.branch[HLT] = lambda _, __: self.hlt()

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def load(self, file):
        for line in file:
            comment_split = line.split("#")
              num = comment_split[0].strip()
               if num == '':
                    continue
                value = int(num, 2)
                self.ram[address] = value
                address += 1

    def alu(self, op, reg_a,reg_b):
      if op == "CMP":
        pass
      else:
        raise Exception("Unsupported ALU branch")

    def run(self):
      while self.running:
        self.IR = self.ram_read(self.PC)
        operand_a = self.read(self.PC +1)
        operand_b = self.read(self.PC +2)
        self.PC += (self.IR >> 6) + 1
        self.branch[self.IR](operand_a,operand_b)

    def ldi(self, mar, mdr):
      self.reg[mar] = mdr

    def hlt(self):
      self.running = False
      sys.exist()

    def prn(self, mar):
      print(self.reg[mar])

    
# ### CMP

# *This is an instruction handled by the ALU.*

# `CMP registerA registerB`

# Compare the values in two registers.

# * If they are equal, set the Equal `E` flag to 1, otherwise set it to 0.

# * If registerA is less than registerB, set the Less-than `L` flag to 1,
#   otherwise set it to 0.

# * If registerA is greater than registerB, set the Greater-than `G` flag
#   to 1, otherwise set it to 0.

# Machine code:
# ```
# 10100111 00000aaa 00000bbb
# A7 0a 0b
# ```

# * `E` Equal: during a `CMP`, set to 1 if registerA is equal to registerB, zero
#   otherwise.

#   ### JMP

# `JMP register`

# Jump to the address stored in the given register.

# Set the `PC` to the address stored in the given register.

# Machine code:
# ```
# 01010100 00000rrr
# 54 0r
# ```

# ### JNE

# `JNE register`

# If `E` flag is clear (false, 0), jump to the address stored in the given
# register.

# Machine code:
# ```
# 01010110 00000rrr
# 56 0r
# ```