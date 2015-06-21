from FSimulator import FunctionalSimulator
import numpy as np
import sys
import getopt

# To print full numpy arrays
np.set_printoptions(threshold=5000)

# Read command line args
try:
    myopts, args = getopt.getopt(sys.argv[1:], "s:")
except getopt.GetoptError as e:
    print(str(e))
    print("Usage: %s -s <scaling factor>" % sys.argv[0])
    sys.exit(2)

SCALE_FACTOR = 1  # default

print(myopts)

for o, a in myopts:
    if o == '-s':
        SCALE_FACTOR = int(a)

print(SCALE_FACTOR)
fname = "program.txt"

MEM_SIZE = 5000
OPERAND_SIZE = 100

# Add two 40x40 matrices and write back the result to memory
# First matrix is at location 0, second one starts at location 1600
# Output is written to location 3200
with open(fname) as f:
    program = [x.strip('\n') for x in f.readlines()]

# Pre-load two 40x40 matrices in memory
mem = np.zeros(MEM_SIZE, dtype=int)
for i in range(3200):
    mem[i] = i

fsim = FunctionalSimulator(SCALE_FACTOR, MEM_SIZE, OPERAND_SIZE)

fsim.set_memory(mem)
fsim.set_program(program)

fsim.print()  # Print initial memory and cycle count
fsim.run_program()
fsim.print()  # Print memory and cycle count after simulating the program

# print(fsim.memory[3200:4800])
