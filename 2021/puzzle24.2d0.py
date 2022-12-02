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

    def setRange(self, registers, min, max = None):
        registers[self.index] = Range(min, max)

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

    def operandValues(self, registers):
        a = self.target.getRange(registers)
        source = self.source
        b = source.getRange(registers) if isinstance(source, Register) \
            else Range(source, source)
        return a, b

class OpInp(Op):

    prefixValues = [ ] # A list of known input values

    def exec(self, registers):
        inputNum = self.source
        if inputNum < len(OpInp.prefixValues):
            val = OpInp.prefixValues[inputNum]
            self.target.setRange(registers, val)
        else:
            self.target.setRange(registers, 1, 9)

class OpAdd(Op):

    def exec(self, registers):
        a, b = self.operandValues(registers)
        self.target.setRange(registers, a.min() + b.min(), a.max() + b.max())

class OpMul(Op):

    def exec(self, registers):
        a, b = self.operandValues(registers)
        minA, maxA = a
        minB, maxB = b
        results = (minA * minB, minA * maxB, maxA * minB, maxA * maxB)
        self.target.setRange(registers, min(results), max(results))

class OpDiv(Op):

    def exec(self, registers):
        a, b = self.operandValues(registers)
        minA, maxA = a
        minB, maxB = b
        assert(minB != 0 and maxB != 0)
        results = (div(minA, minB), div(minA, maxB),
                   div(maxA, minB), div(maxA, maxB))
        self.target.setRange(registers, min(results), max(results))

class OpMod(Op):

    def exec(self, registers):
        a, b = self.operandValues(registers)
        minA, maxA = a
        minB, maxB = b
        assert(minB > 0 and maxB > 0)
        results = (minA % minB, minA % maxB, maxA % minB, maxA % maxB)
        self.target.setRange(registers, min(results), max(results))

class OpEql(Op):

    def exec(self, registers):
        a, b = self.operandValues(registers)
        if a.max() < b.min() or a.min() > b.max():
            self.target.setRange(registers, 0)  # No overlap in ranges
        elif a.max() == b.min() and a.min() == b.max():
            self.target.setRange(registers, 1)  # All the same values
        else:
            self.target.setRange(registers, 0, 1)  # Could be equal or not

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
    source = None
    if len(operands) < 2:
        assert(opcode == 'inp')
        source = inputCount
        inputCount += 1
    else:
        if operands[1] in 'wxyz':
            source = Register(ord(operands[1]) - ord('w'))
        else:
            source = int(operands[1])
    operation = operations[opcode]
    return operation(target, source)

def solve(registers, instructions, firstInstr = 0, inputPrefix = [ ]):
    """Try to find a solution where `instructions` leaves a zero value in
    `registers[z]` by appending to the initial sequence of inputs specified in
    `inputPrefix`.  If successful, returns the complete list of 14 inputs that
    solves the expression.  If unsuccessful, returns `None`.
    """

    if len(inputPrefix) > 14:
        return inputPrefix  # Solved!

    for i in range(1, 10):
        savePrefix = OpInp.prefixValues
        tryInputPrefix = inputPrefix + [ i ]
        OpInp.prefixValues = tryInputPrefix
        tryRegisters = registers.copy()
        lastInput      = len(instructions)
        regsAfterInput = [ ]
        # Execute instructions up to and including an `OpInp` instruction
        for instIndex in range(firstInstr, len(instructions)):
            instruction = instructions[instIndex]
            instruction.exec(tryRegisters)
            if isinstance(instruction, OpInp):
                # Take snapshot after `OpInp` instruction
                assert(instruction.source == len(inputPrefix))
                lastInput      = instIndex
                regsAfterInput = tryRegisters.copy()
                break
        # Execute the remaining instructions
        for instIndex in range(lastInput + 1, len(instructions)):
            instruction = instructions[instIndex]
            instruction.exec(tryRegisters)
        OpInp.prefixValues = savePrefix  # Pop prefix

        minE, maxE = tryRegisters[3]  # Z register
        if minE <= 0 and 0 <= maxE:
            # Found partial solution.  Recurse down another level.
            # Nested levels can start after last input, since everything up to
            # that point is fixed.
            if len(inputPrefix) < 8:
                print("\rPartial = %-15s" % ''.join(map(lambda x : str(x), tryInputPrefix)), end='')
            solution = solve(regsAfterInput, instructions, lastInput + 1, tryInputPrefix)
            if solution: return solution  # Solved!

    return None

infile = open("puzzle24_input.txt", "r")

instructions = [ ]

for instrStr in infile:
    instructions.append(parseInstr(instrStr))

print(f'{len(instructions)} instructions processed, solving...')

solution = solve([ Range(0, 0) ] * 4, instructions)
print("\nSolution =", ''.join(map(lambda x : str(x), solution)))
