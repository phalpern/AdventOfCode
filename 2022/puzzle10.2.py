#! /usr/bin/python3

# Usage: puzzleXX.Y.py [input-suffix]
#
# Where XX is the puzzle number in decimal (with leading zero, if necessary)
# and Y is the sub-part (1 or 2).  By default, the input-suffix is "input", so
# the input file would be "puzzleXX_input.txt".  Note that the input to the two
# parts of one puzzle is typically the same file, so Y does not show up in the
# default input file name.

import sys
import openInput

input = openInput.openInput(sys.argv)

class Cpu:
    """Abstraction of the simple CPU"""

    # Opcodes (class "constants")
    noop = 0
    addx = 1
    opcodes = { "noop" : noop, "addx" : addx }

    def __init__(self, program):
        """Create a CPU instance to run the specified `program`, where
        `program` is an iterable over a sequence of instructions. Each
        instruction is a tuple of the form (opcode, value), where `value` is
        optional."""
        self.x      = 1              # x register
        self.cycle  = 1              # Cycle that is about to start
        self.pc     = iter(program)  # Program counter for traversing the input
        self.addend = None           # operand for addx instruction in progress

    def run(self, cycles):
        """Advance program by `cycles`. The final state might be in the middle
        of an instruction."""
        for cycleCounter in range(0, cycles):
            if self.addend is None:
                # Not in the middle of an addx instruction
                opcode, *operands = next(self.pc)
                if opcode == Cpu.noop:
                    pass;
                elif opcode == Cpu.addx:
                    self.addend = operands[0]
                else:
                    assert(False)  # unknown opcode
            else:
                # Second cycle of addx instruction
                self.x += self.addend
                self.addend = None
            self.cycle += 1

    def __str__(self):
        return f"x = {self.x} at cycle {self.cycle}"

program = [ ]
for line in input:
    opcodestr, *operandStrs = line.split()
    opcode = Cpu.opcodes[opcodestr]
    if operandStrs:
        instruction = (opcode, int(operandStrs[0]))
    else:
        instruction = (opcode, )
    program.append(instruction)

theCpu = Cpu(program)
pixels = ""
try:
    for row in range(0, 6):
        for col in range(0, 40):
            pixels += '#' if theCpu.x - 1 <= col and col <= theCpu.x + 1 else '.'
            theCpu.run(1)
except(StopIteration):
    pass

for i in range(0, 240, 40):
    print(pixels[i:i+40])
