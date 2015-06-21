This package contains the following files:

README.txt: describes the set-up, usage and other details
switch.py: Python class to emulate C-style switch-case statements (Ref: 2)
FSimulator.py: Functional Simulator, which can be configured as a distributed simulator
program.txt: Sample program to sum add 40x40 matrices element-wise and write result to memory
run.py: Python script to simulate program.txt using FSimulator

Python version used is 3.4.3, tested on Mac OS 10.10.2

-----------------------------------------------------------
Usage of run.py
-----------------------------------------------------------
python run.py -s <scaling factor>

To simulate program.txt with one compute node, use

    "python run.py" (default scaling factor of 1)

This takes 16 simulation cycles.

To simulate program.txt with four compute nodes, use
    "python run.py -s 4"

This takes 4 simulation cycles.

In both the cases, the following get printed:
    initial memory contents, initial cycle count
    instructions being executed
    final memory contents, final cycle count

The run script pre-loads the memory with two 40x40 matrices
The first matrix starts at offset 0.
The second matrix starts at offset 1600.
The values of these matrices are equal to the memory index

The run script also extracts program from program.txt

-----------------------------------------------------------
Program specification (Domain specific language)
-----------------------------------------------------------
The program itself is specified in simple assembly.

Instruction format is:
    OPCODE OPTR IPTR1 IPTR2

Supported OPCODES are bit-wise AND/OR/XOR/NOR and ADD, SUB
and MULTIPLY performed element-wise

All three pointers are start indices to memory

-----------------------------------------------------------
Functional Simulator
-----------------------------------------------------------

The concepts are borrowed/inspired from online (Ref:1)

Once the program is fed and memory is initialized, the
run_program() method simulates one or more instructions
in one cycle. The number of instructions processed in
one cycle is equal to scaling factor (by design)

When scaling factor is 1, the three phases read, execute
and write of one instruction is simulated in one cycle.

When scaling factor is 4, the simulator processes four
instructions of the program at a time. The parallel
processing is implemented as follows:
    a. Decode four successive instructions in program
    b. Read four pairs of input operands from memory
    c. Execute arithmetic on these four pairs
    d. Write the four results to memory

Simulator is incapable of detecting data hazards.
During write phase, the simulator updates memory in
sequence of instructions, although it could be
unpredictable in reality

-----------------------------------------------------------
In-built checks in functional simulator
-----------------------------------------------------------
The functional simulator checks that the pointers are legal
and the program size is a multiple of scaling factor

-----------------------------------------------------------
Validation
-----------------------------------------------------------
A basic level of validation is performed on this simulator
The given program is tested/found to be functionally correct

Contact: opraveen@gmail.com for any questions

-----------------------------------------------------------
References
-----------------------------------------------------------
1. http://www.pythondiary.com/blog/Oct.15,2014/building-cpu-simulator-python.html
2. http://code.activestate.com/recipes/410692/



