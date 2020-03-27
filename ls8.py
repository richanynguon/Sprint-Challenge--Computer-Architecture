import sys
from cpu import *

cpu = CPU()
with open(sys.argv[1]) as file:
    cpu.load(file)

cpu.run()