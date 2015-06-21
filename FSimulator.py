import numpy as np
from switch import Switch

class FunctionalSimulator(object):
    """
    This class is the Functional Simulator of a hypothetical computer system
    Implementation notes:
    1. Only data-memory is modeled, code is provided separately as a "program"
    2. Data granularity is 10x10 matrix
    3. Map three phases of a simulator cycle to execution of a single instruction in program
    4. Domain-specific assembly language: OPCODE OPTR IPTR1 IPTR2
        a. OPCODE: Supported Arithmetic: ADD, AND, OR, XOR, ..
        b. OPTR: Memory Pointer to output data. Data sized constrained to 100 elements
        d. OPTR: Memory Pointer to input1 data. Data sized constrained to 100 elements
        b. OPTR: Memory Pointer to input2 data. Data sized constrained to 100 elements
    5. Data unit of size 10x10 matrix is mapped to contiguous locations in memory
    6. For distributed simulator, each of the three phases would handle 4 instructions at a time
        a. simulator is agnostic to data hazards
        b. example program in our case is highly parallel. So, without loss of generality, the program
            itself is unchanged, and the simulator interprets/processes the program as per the scaling_factor
    7. To configure simulator as a distributed simulator of 4 compute nodes, use scale_factor=4
    """

    def __init__(self, scale_factor=1, mem_size=5000, operand_size=100):
        """
        Constructor
        :param scale_factor: Specifies the factor of parallelism in system
        :param mem_size: Size of data memory
        :param operand_size: Size of operand or data
        :return: void
        """
        self.scale_factor = scale_factor
        self.mem_size = mem_size
        self.operand_size = operand_size

        self.memory = np.zeros(mem_size, dtype=int)

        self.program = []  #: Program/code to be simulated
        self.pc = 0

        # Current cycle (current instruction) processing data
        self.input1 = np.zeros((operand_size, scale_factor))
        self.input2 = np.zeros((operand_size, scale_factor))
        self.output = np.zeros((operand_size, scale_factor))

        self.cycles = 0

    def set_memory(self, mem):
        """
        Provision to initialize or backdoor-load data memory

        """
        self.memory = mem

    def set_program(self, code):
        """
        Program to be simulated

        """
        self.program = code
        # self.pc = 0  #: Just points to the program index, in this case

        if len(self.program) % self.scale_factor:
            print("Program size", len(self.program), "not a multiple of scale_factor ", self.scale_factor)
            exit()

    def reset(self):
        """
        Reset the simulator

        """
        self.pc = 0
        self.cycles = 0

    def run_program(self):
        """
        Run Program:
        Single instruction simulation includes three phases:
        1. Read two 10x10 matrices from self.memory
        2. Perform arithmetic
        3. Write back 10x10 matrix result to self.memory

        "scale_factor" number of instructions are simulated in one cycle
        """

        # Create lists to hold data for multiple nodes
	# Alternately, we could use numpy arrays
        opcode = [None]*self.scale_factor
        optr = [None]*self.scale_factor
        iptr1 = [None]*self.scale_factor
        iptr2 = [None]*self.scale_factor

        # Reset program counter
        self.pc = 0

        while self.pc < len(self.program):

            # One cycle operation:

            # Decode instruction
            for i in range(self.scale_factor):

                # Format of the instruction is {OPCODE OPTR IPTR1 IPTR2}
                instr = self.program[self.pc+i].split()

                print("Instruction: ", instr)

                opcode[i] = instr[0]

                optr[i] = int(instr[1])
                iptr1[i] = int(instr[2])
                iptr2[i] = int(instr[3])

            # Read phase
            for i in range(self.scale_factor):
                self.read_phase(iptr1[i], iptr2[i], i)

            # Execute/Arithmetic phase
            for i in range(self.scale_factor):
                self.arithmetic_phase(opcode[i], i)

            # Write phase
            for i in range(self.scale_factor):
                self.write_phase(optr[i], i)

            self.cycles += 1

    def read_phase(self, ptr1, ptr2, node):
        """
        Read operands phase

        """
        if ptr1 < 0 or ptr1 > (self.mem_size-self.operand_size) or \
           ptr2 < 0 or ptr2 > (self.mem_size-self.operand_size):
            print("Error! Unacceptable input operand(s): ptr1=", ptr1, "ptr2=", ptr2)
            exit()

        self.input1[:, node] = self.memory[ptr1:ptr1+self.operand_size]
        self.input2[:, node] = self.memory[ptr2:ptr2+self.operand_size]

    def arithmetic_phase(self, operation, node):
        """
        Arithmetic phase

        """
        for case in Switch(operation):
            if case('AND'):
                self.output[:, node] = np.bitwise_and(self.input1[:, node], self.input2[:, node])
                break
            if case('OR'):
                self.output[:, node] = np.bitwise_or(self.input1[:, node], self.input2[:, node])
                break
            if case('XOR'):
                self.output[:, node] = np.bitwise_xor(self.input1[:, node], self.input2[:, node])
                break
            if case('NOR'):
                self.output[:, node] = np.bitwise_nor(self.input1[:, node])  # Single operand instruction
                break
            if case('ADD'):
                self.output[:, node] = np.add(self.input1[:, node], self.input2[:, node])
                break
            if case('SUB'):
                self.output[:, node] = np.subtract(self.input1[:, node], self.input2[:, node])
                break
            if case('MULT'):
                self.output[:, node] = np.multiply(self.input1[:, node], self.input2[:, node])
                break
            if case():  # Default
                print("Error! Undefined instruction ", operation)
                exit()

    def write_phase(self, ptr, node):
        """
        Write phase

        """
        if ptr < 0 or ptr > (self.mem_size-self.operand_size):
            print("Error! Unacceptable output operand: ptr=", ptr)
            exit()

        self.memory[ptr:ptr+self.operand_size] = self.output[:, node]

        # Increment program counter upon completion of write phase
        self.pc += 1

    def print(self):
        """
        Print memory and cycle count

        """
        print(self.memory)
        print("Number of cycles = ", self.cycles)
