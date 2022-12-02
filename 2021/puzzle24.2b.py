# Advent of code day 24, part 1
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

inputRanges = [None]

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

def getOpcode(expression):
    if isinstance(expression, int):
        return 'int'
    else:
        return expression[0]

def getRange(expression):
    """Return the result closed range of the expression as a list [min, max]."""
    if isinstance(expression, int):
        # Expression is a scalar integer
        return [expression, expression]
    else:
        # Expression is a tuple ('opcode', [min, max], operands...).
        # Return (min, max)
        return expression[1]

def setRange(opTuple, newRange):
    """Replace the range in the specified opTuple"""
    assert(newRange[0] <= newRange[1])
    opTuple[1][0] = newRange[0]
    opTuple[1][1] = newRange[1]

def getOperands(opTuple):
    """Return a tuple of one or two operands from `opTuple`"""
    return opTuple[2:]

def replaceRange(opTuple, newRange):
    """Replace the range in `opTuple` with `newRwange` and return the modified
    tuple, except when `newRange` describes a single value, in which case
    discard the tuple and return the value."""
    if newRange[0] == newRange[1]:
        return newRange[0]   # Replace entire tuple with scalar
    else:
        setRange(opTuple, newRange)
        return opTuple

def opInp(opTuple):
    (operand,) = getOperands(opTuple)
    if operand < len(inputRanges):
        range = inputRanges[operand]
    else:
        range = [1, 9]
    return replaceRange(opTuple, range)

def opAdd(opTuple):
    a, b = getOperands(opTuple)
    if a == 0:
        return b
    elif b == 0:
        return a
    elif isinstance(a, int) and isinstance(b, int):
        return a + b
    else:
        minA, maxA = getRange(a)
        minB, maxB = getRange(b)
        return replaceRange(opTuple, [minA + minB, maxA + maxB])

def opMul(opTuple):
    a, b = getOperands(opTuple)
    if a == 0 or b == 0:
        return 0
    elif a == 1:
        return b
    elif b == 1:
        return a
    elif isinstance(a, int) and isinstance(b, int):
        return a * b
    else:
        minA, maxA = getRange(a)
        minB, maxB = getRange(b)
        minR = min((minA*minB, minA*maxB, maxA*minB, maxA*maxB))
        maxR = max((minA*minB, minA*maxB, maxA*minB, maxA*maxB))
        return replaceRange(opTuple, [minR, maxR])

def opDiv(opTuple):
    a, b = getOperands(opTuple)
    minA, maxA = getRange(a)
    minB, maxB = getRange(b)
    # TBD: Not sure the next three lines are correct for check-and-go
    if minB == 0: minB = 1    # Narrow range knowing no divide-by-zero
    if maxB == 0: maxB = -1   # Narrow range knowing no divide-by-zero
    if minB == maxB: b = minB # Convert to scalar?
    if a == 0:
        return 0
    elif b == 1:
        return a
    elif isinstance(a, int) and isinstance(b, int):
        return div(a, b)
    elif a == b:
        return 1
    else:
        minR = min((div(minA, minB), div(minA, maxB), div(maxA, minB), div(maxA, maxB)))
        maxR = max((div(minA, minB), div(minA, maxB), div(maxA, minB), div(maxA, maxB)))
        if minR == maxR: return minR  # Convert to scalar?
        return replaceRange(opTuple, [minR, maxR])

def opMod(opTuple):
    a, b = getOperands(opTuple)
    minA, maxA = getRange(a)
    minB, maxB = getRange(b)
    if minA < 0: minA = 0   # Narrow range knowing no negative values
    if minB < 1: minB = 1   # Narrow range knowing no values < 1
    if minA == maxA: a = minA # Convert to scalar?
    if minB == maxB: b = minB # Convert to scalar?
    if a == 0:
        return 0
    elif b == 1:
        return 0
    elif isinstance(a, int) and isinstance(b, int):
        return a % b
    elif maxA < minB:
        assert(a[1][0] == minA)  # If fails, then we need to rebuld a with new range
        return a
    else:
        return replaceRange(opTuple, [0, min((maxA, maxB - 1))])

def opNot(opTuple):
    """Synthetic opcode 'not'. Does not directly show up in input file."""
    (a,) = getOperands(opTuple)
    if isinstance(a, int):
        return 1 - a
    nestedOpcode, nestedRange, *nestedOperands = a
    if nestedOpcode == 'not':
        return nestedOperands[0] # Double negation
    else:
        return replaceRange(opTuple, [0, 1])

def isBool(expression):
    """Return true if the range for `expression` is (0, 1)"""
    return [0, 1] == getRange(expression)

def opEql(opTuple):
    a, b = getOperands(opTuple)
    if a == b:
        return 1
    elif isinstance(a, int) and isinstance(b, int):
        return 0  # a != b for known values a and b
    else:
        minA, maxA = getRange(a)
        minB, maxB = getRange(b)
        if minB > maxA or minA > maxB:
            return 0  # No overalap, cannot be equal
        if isBool(a):
            if 0 == b:
                return opNot(('not', [0, 1], a))
            elif 1 == b:
                return a
        elif isBool(b):
            if 0 == a:
                return opNot(('not', [0, 1], b))
            elif 1 == a:
                return b
        return replaceRange(opTuple, [0, 1])

operations = {
    'inp' : opInp,
    'add' : opAdd,
    'mul' : opMul,
    'div' : opDiv,
    'mod' : opMod,
    'eql' : opEql,
    'not' : opNot
}

inputCount = 0

def processInstr(registers, instrStr):
    """Process the specified instruction, modifying the registers. Processing
    involves updating the instruction tree for a register.  No I/O actually
    occurs."""
    global inputCount
    opcode, *operands = instrStr.rstrip().split(' ')
    target = operands[0]
    arg1 = registers[target]
    arg2 = None
    if len(operands) < 2:
        if opcode == 'inp':
            inputCount += 1
        arg1 = inputCount
        opTuple = (opcode, [INTMIN, INTMAX], arg1)
    else:
        if operands[1] in 'wxyz':
            arg2 = registers[operands[1]]
        else:
            arg2 = int(operands[1])
        opTuple = (opcode, [INTMIN, INTMAX], arg1, arg2)
    operation = operations[opcode]
    result = operation(opTuple)
    registers[target] = result

def simplify(expression):
    """Recursively simplify `expression` and return the simplification"""
    if not isinstance(expression, tuple):
        return expression  # Leaf expression; no simplification possible

    opcode, range, *operands = expression  # Unpack
    simplifiedOps = [ simplify(operands[0]) ]
    if opcode == 'inp':
        pass
    elif len(operands) < 2:
        if simplifiedOps[0] is operands[0]:
            return expression  # Nothing got simplified
    else:
        simplifiedOps.append(simplify(operands[1]))
        if simplifiedOps[0] is operands[0] and simplifiedOps[1] is operands[1]:
            return expression  # Nothing got simplified

    operation = operations[opcode]
    return operation((opcode, range, *simplifiedOps))

def getInputSet(expression, inset = set()):
    if not isinstance(expression, tuple):
        return inset

    opcode, range, *operands = expression  # Unpack
    if opcode == 'inp':
        inset.add(operands[0])
        return inset
    inset = getInputSet(operands[0], inset)
    if len(operands) > 1: inset = getInputSet(operands[1], inset)
    return inset

def solve(expression, inputPrefix = [None]):
    """Try to find a solution where `expression` evaluates to zero using the
    initial sequence of inputs specified in `inputPrefix`.  If successful,
    returns the complete list of 14 inputs that solves the expression.  If
    unsuccessful, returns `None`."""
    global inputRanges
    if len(inputPrefix) > 14:
        return inputPrefix  # Solved!

    for i in range(1, 10):
        tryInputList =  inputPrefix + [[i, i]]
        inputRanges = tryInputList
        simplifiedExpr = simplify(expression)
        minE, maxE = getRange(simplifiedExpr)
        if minE <= 0 and 0 <= maxE:
            # Found partial solution.  Recurse down another level.
            inputSet = getInputSet(simplifiedExpr)
            if len(inputSet) + len(inputPrefix) < 15:
                print("\nLimited input set,", inputSet, "for partial",''.join(map(lambda x : str(x[0]), tryInputList[1:])))
            if len(inputPrefix) < 8:
                print("\rPartial = %-15s" % ''.join(map(lambda x : str(x[0]), tryInputList[1:])), end='')
            solution = solve(simplifiedExpr, tryInputList)
            if solution: return solution  # Solved!

    inputRanges = inputPrefix  # Pop list
    return None

infile = open("puzzle24_input.txt", "r")

registers = {
    'w' : 0,
    'x' : 0,
    'y' : 0,
    'z' : 0
    }

for instrStr in infile:
    processInstr(registers, instrStr)

def depth(x, d = 0):
    assert(d < 1000)
#    print("\rDepth so far ", d, "   ", end='')
    maxDepth = d
    if isinstance(x, tuple):
        for y in x:
            maxDepth = max((maxDepth, depth(y, d + 1)))
    return maxDepth

print('Input processed, solving...')
solution = solve(registers['z'])
print("\nSolution =", ''.join(map(lambda x : str(x[0]), solution[1:])))
