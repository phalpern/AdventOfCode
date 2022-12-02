# Advent of code day 24, part 2
# Find smallest MONAD model number

import sys

# The registers dictionary maps each register to a tree. Each tree node is
# either an integer leaf value or a tuple, (opcode, [minValue, maxValue],
# leftNode, rightNode), where the right operand is optional.  The [minValue,
# maxValue] list is deliberately mutable so that it can be updated during
# subsequent traversals tree.

# Although integers have indefinite precision, for our purposes here, we can
# choose meaningful max and min values.
INTMAX = sys.maxsize
INTMIN = -INTMAX

class Register:
    def __init__(self, index):
        assert(isinstance(index, int))
        self.index = index

    def getRange(self, registers):
        return registers[self.index]

    def setRange(self, registers, min, max = None):
        if max is None: max = min
        assert(isinstance(min, int) and isinstance(max, int))
        registers[self.index] = (min, max)

def div(a, b, roundingMode = 'zero'):
    """Return a / b, with rounding mode = 'zero', 'floor', or 'ceiling'"""

    if roundingMode == 'zero':
        isneg = (a < 0) != (b < 0)
        roundingMode = 'ceiling' if isneg else 'floor'

    if roundingMode == 'floor':
        return a // b
    elif roundingMode == 'ceiling':
        return -(-a // b)
    else:
        assert(False and 'Invalid rounding mode')

class Op:
    def __init__(self, target, source):
        self.target = target
        self.source = source

    def operandValues(self, registers):
        a = self.target.getRange(registers)
        source = self.source
        b = source.getRange(registers) if isinstance(source, Register) \
            else (source, source)
        return a, b

class OpInp(Op):

    prefixValues = [None] # A list of known input values

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
        self.target.setRange(registers, a[0] + b[0], a[1] + b[1])

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
        if a[1] < b[0] or a[0] > b[1]:
            self.target.setRange(registers, 0)  # No overlap in ranges
        elif a[1] == b[0] and a[0] == b[1]:
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
        inputCount += 1
        source = inputCount
    else:
        if operands[1] in 'wxyz':
            source = Register(ord(operands[1]) - ord('w'))
        else:
            source = int(operands[1])
    operation = operations[opcode]
    return operation(target, source)

def runInstructions(registers, instructions, firstInstr, inputPrefix):
    """
    Modify the `registers` by executing the list of `instructions` starting
    from the instruction at index, `firstInstr`.  The `inputPrefix` is a list
    of the first n known input values, where n is `len(inputPerfix) - 1)
    """
    savePrefix = OpInp.prefixValues
    OpInp.prefixValues = inputPrefix
    for instIndex in range(firstInstr, len(instructions)):
        instructions[instIndex].exec(registers)
    OpInp.prefixValues = savePrefix

def solve(registers, instructions, firstInstr = 0, inputPrefix = [None]):
    """Try to find a solution where `instructions` leaves a zero value in
    `registers[z]` by appending to the initial sequence of inputs specified in
    `inputPrefix`.  If successful, returns the complete list of 14 inputs that
    solves the expression.  If unsuccessful, returns `None`.
    """

    if len(inputPrefix) > 14:
        return inputPrefix  # Solved!

    for i in range(1, 10):
        tryInputList = inputPrefix + [ i ]
        tryRegisters = registers.copy()
        runInstructions(tryRegisters, instructions, firstInstr, tryInputList)
        minE, maxE = tryRegisters[3]  # Z register
        if minE <= 0 and 0 <= maxE:
            # Found partial solution.  Recurse down another level.
            if len(inputPrefix) < 8:
                print("\rPartial = %-15s" % ''.join(map(lambda x : str(x), tryInputList[1:])), end='')
            # TBD: optimize by updating `firstInstr` and using `tryRegisters`
            solution = solve(registers, instructions, firstInstr, tryInputList)
            if solution: return solution  # Solved!

    return None

infile = open("puzzle24_input.txt", "r")

instructions = [ ]

for instrStr in infile:
    instructions.append(parseInstr(instrStr))

print(f'{len(instructions)} instructions processed, solving...')

solution = solve([ (0, 0) ] * 4, instructions)
print("\nSolution =", ''.join(map(lambda x : str(x), solution[1:])))
