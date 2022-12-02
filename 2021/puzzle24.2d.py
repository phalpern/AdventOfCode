# Advent of code day 24, part 2
# Find smallest MONAD model number

import sys

class Range(tuple):
    def __new__(cls, min, max = None):
        if max is None: max = min
        assert(isinstance(min, int) and isinstance(max, int) and min <= max)
        return super().__new__(cls, (min, max))

    def min(self):
        return self[0]

    def max(self):
        return self[1]

class Register:
    def __init__(self, index):
        assert(isinstance(index, int))
        self.index = index

    def getRange(self, registers):
        return registers[self.index]

    def setRange(self, registers, range):
        registers[self.index] = range

def div(a, b):
    """Return a / b, rounded towards zero.  This function differs from // in
    that the latter operator rounds towards negative."""

    if (a < 0) != (b < 0):
        # Result will be negative. Round towards zero by negating, rounding
        # (tawards negative), and negating again.
        return -(-a // b)
    else:
        # Result will be positive. Round towards negative == round towards
        # zero.
        return a // b

class Op:
    def __init__(self, target, source):
        self.target = target
        self.source = source

    def exec(self, registers):
        a = self.target.getRange(registers)
        source = self.source
        b = source.getRange(registers) if isinstance(source, Register) \
            else Range(source, source)
        self.target.setRange(registers, self.execImp(a, b))

class OpInp(Op):

    prefixValues = [None] # A list of known input values

    def execImp(self, a, b):
        inputNum = b.min()
        if inputNum < len(OpInp.prefixValues):
            return Range(OpInp.prefixValues[inputNum])
        else:
            return Range(1, 9)

class OpAdd(Op):

    def execImp(self, a, b):
        return Range(a.min() + b.min(), a.max() + b.max())

class OpMul(Op):

    def execImp(self, a, b):
        minA, maxA = a
        minB, maxB = b
        results = (minA * minB, minA * maxB, maxA * minB, maxA * maxB)
        return Range(min(results), max(results))

class OpDiv(Op):

    def execImp(self, a, b):
        minA, maxA = a
        minB, maxB = b
        assert(minB != 0 and maxB != 0)
        results = (div(minA, minB), div(minA, maxB),
                   div(maxA, minB), div(maxA, maxB))
        return Range(min(results), max(results))

class OpMod(Op):

    def execImp(self, a, b):
        minA, maxA = a
        minB, maxB = b
        assert(minB > 0 and maxB > 0)
        results = (minA % minB, minA % maxB, maxA % minB, maxA % maxB)
        return Range(min(results), max(results))

class OpEql(Op):

    def execImp(self, a, b):
        if a.max() < b.min() or a.min() > b.max():
            return Range(0)  # No overlap in ranges
        elif a.max() == b.min() and a.min() == b.max():
            return Range(1)  # All the same values
        else:
            return Range(0, 1)  # Could be equal or not

operations = {
    'inp' : OpInp,
    'add' : OpAdd,
    'mul' : OpMul,
    'div' : OpDiv,
    'mod' : OpMod,
    'eql' : OpEql
}

inputCount = 0  # Number of input instructions parsed

def parseInstr(instrStr):
    """Parse the specified instruction string and return the compiled `Op` object."""
    global inputCount
    opcode, *operands = instrStr.rstrip().split(' ')
    target = Register(ord(operands[0]) - ord('w'))
    operation = operations[opcode]
    if operation is OpInp:
        assert(len(operands) < 2)
        inputCount += 1
        return OpInp(target, inputCount)
    elif operands[1] in 'wxyz':
        return operation(target, Register(ord(operands[1]) - ord('w')))
    else:
        return operation(target, int(operands[1]))

def solve(startRegisters, instructions, startInstr = 0, startInpPrefix = [None]):
    """Try to find a solution where `instructions` leaves a zero value in
    `startRegisters[z]` by appending to the initial sequence of inputs specified in
    `startInpPrefix`.  If successful, returns the complete list of 14 inputs that
    solves the expression.  If unsuccessful, returns `None`.
    """

    if len(startInpPrefix) > 14:
        return startInpPrefix  # Solved!

    inpPrefix = startInpPrefix + [ 0 ]
    for i in range(1, 10):
        inpPrefix[-1] = i
        OpInp.prefixValues = inpPrefix
        registers = startRegisters.copy()
        nextGroupInstr = len(instructions)
        nextGroupRegs  = [ ]
        # Execute instructions up to and including an `OpInp` instruction
        for instIndex in range(startInstr, len(instructions)):
            instruction = instructions[instIndex]
            instruction.exec(registers)
            if isinstance(instruction, OpInp):
                # Take snapshot after `OpInp` instruction
                assert(instruction.source == len(startInpPrefix))
                nextGroupInstr = instIndex + 1
                nextGroupRegs  = registers.copy()
                break
        # Execute the remaining instructions
        for instIndex in range(nextGroupInstr, len(instructions)):
            instruction = instructions[instIndex]
            instruction.exec(registers)

        minE, maxE = registers[3]  # z register
        if minE <= 0 and 0 <= maxE:
            # Found partial solution.  Recurse down another level.
            # Nested levels can start after last input, since everything up to
            # that point is fixed.
            # if len(inpPrefix) < 9:
            #     print("\rPartial = %-15s" % ''.join(map(lambda x : str(x), inpPrefix[1:])), end='')
            solution = solve(nextGroupRegs, instructions, nextGroupInstr, inpPrefix)
            if solution: return solution  # Solved!

    return None

infile = open("puzzle24_input.txt", "r")

instructions = [ ]

for instrStr in infile:
    instructions.append(parseInstr(instrStr))

print(f'{len(instructions)} instructions processed, solving...')

solution = solve([ Range(0, 0) ] * 4, instructions)
print("\nSolution =", ''.join(map(lambda x : str(x), solution[1:])))
