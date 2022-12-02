# Advent of code day 24, part 1
# Find largest MONAD model number

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

def getRange(operand):
    """Return the result closed range of the operand as a tuple (min, max)."""
    if isinstance(operand, int):
        # Operand is a scalar integer
        return [operand, operand]
    else:
        # Operand is a tuple ('opcode', [min, max], operands...).
        # Return (min, max)
        return operand[1]

def setRange(operand, newRange):
    operand[1][0] = newRange[0]
    operand[1][1] = newRange[1]

input = 0
def opInp(a, b):
    global input
    input += 1
    if input <= 2:
        return ('inp', [9, 9], input)
    elif input <= 3:
        return ('inp', [2, 2], input)
    elif input <= 4:
        return ('inp', [9, 9], input)
    return ('inp', [1, 9], input)

def opAdd(a, b):
    if a == 0:
        return b
    elif b == 0:
        return a
    elif isinstance(a, int) and isinstance(b, int):
        return a + b
    else:
        minA, maxA = getRange(a)
        minB, maxB = getRange(b)
        return ('add', [minA + minB, maxA + maxB], a, b)

def opMul(a, b):
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
        return ('mul', [minR, maxR], a, b)

def opDiv(a, b):
    minA, maxA = getRange(a)
    minB, maxB = getRange(b)
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
        return ('div', [minR, maxR], a, b)

def opMod(a, b):
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
        return ('mod', [0, min((maxA, maxB - 1))], a, b)

def isBool(operand):
    """Return true if the range for `operand` is (0, 1)"""
    return [0, 1] == getRange(operand)

def opNot(a):
    """Synthetic opcode 'not'. Does not directly show up in input file."""
    if isinstance(a, int):
        return 1 - a
    opcode, range, *operands = a
    if a[0] == 'not':
        return operands[0] # Double negation
    else:
        return ('not', [0, 1], a)

def opEql(a, b):
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
                return opNot(a)
            elif 1 == b:
                return a
        elif isBool(b):
            if 0 == a:
                return opNot(b)
            elif 1 == a:
                return b
        return ('eql', [0, 1], a, b)

operations = {
    'inp' : opInp,
    'add' : opAdd,
    'mul' : opMul,
    'div' : opDiv,
    'mod' : opMod,
    'eql' : opEql
}

def processInstr(registers, instrStr):
    """Process the specified instruction, modifying the registers. Processing
    involves updating the instruction tree for a register.  No I/O actually
    occurs."""
    opcode, *operands = instrStr.rstrip().split(' ')
    target = operands[0]
    arg1 = registers[target]
    arg2 = None
    if len(operands) > 1:
        if operands[1] in 'wxyz':
            arg2 = registers[operands[1]]
        else:
            arg2 = int(operands[1])
    operation = operations[opcode]
    result = operation(arg1, arg2)
    registers[target] = result

def solveForMultiplicand(product, op1, findLargest):
    """Find the largest or smallest multiplicand that will make
    `op1 * multiplicand == product`.  The `findLargest` argument is
    `True` if we want to find the largest solution,
    `False` if we want to find the smallest."""
    if op1 == 0:
        return INTMAX if findLargest else INTMIN
    return div(product, op1, ('floor', 'ceiling')[findLargest])

def solveForNumerator(quotient, denominator, findLargest):
    """Find the largest or smallest numerator that will make `numerator /
    denominator == quotient` (using round-towards-zero division).  The
    `findLargest` argument is `True` if we want to find the largest solution,
    `False` if we want to find the smallest."""
    # Keep track of whether we are looking for largest absolute value.
    # Note that largest negative value is smallest absolute value.
    findLargestAbs = findLargest
    if quotient < 0:
        quotient = -quotient
        findLargestAbs = not findLargestAbs
    if denominator < 0:
        denominator = -denominator
        findLargestAbs = not findLargestAbs

    if findLargestAbs:
        numerator = (quotient + 1) * denominator - 1
    else:
        numerator = quotient * denominator
    if findLargest != findLargestAbs: numerator = -numerator
    assert(div(numerator, denominator) == quotient)
    return numerator

def solveForDenominator(quotient, numerator, findLargest):
    """Find the largest or smallest denominator that will make 'numerator /
    denominator == quotient' (using round-towards-zero division).  The
    'findLargest' argument is `True` if we want to find the largest solution,
    `False` if we want to find the smallest."""

    # Keep track of whether we are looking for largest absolute value.
    # Note that largest negative value is smallest absolute value.
    findLargestAbs = findLargest
    if quotient < 0:
        quotient = -quotient
        findLargestAbs = not findLargestAbs
    if numerator < 0:
        numerator = -numerator
        findLargestAbs = not findLargestAbs

    if findLargestAbs:
        # If quotient is zero, then maxDeominator is inf, but
        # `INTMAX` is close enough for our purposes.
        if quotient == 0:
            denominator = INTMAX
        else:
            denominator = numerator / quotient
    else:
        denominator = numerator / (quotient + 1) - 1
    if findLargest != findLargestAbs: denominator = -denominator
    assert(div(numerator, denominator) == quotient)
    return denominator

def applySolver(resultRange, knownOpRange, toSolveOpRange, solver):
    """Given a known range for the result of an operation (`resultRange`), a
    known range for one operand (`knownOpRange`), and the initial range for the
    other operand (`toSolveOpRange`), find and return a subset of
    'toSolveOpRange' that will produce values in the `resultRange`.  The
    `solver` function is a 3-operand function that is used to compute solution
    values given one operand from 'resultRange', one from 'knownOpRange', and a
    boolean value of `True` to find a max value or `False` to find a min value.
    The `solver` is applied to each of the 4 combinations to solve for the min
    and max values of the unsolved operand range."""

    rMin, rMax = resultRange
    koMin, koMax = knownOpRange
    tsoMin, tsoMax = toSolveOpRange
    solvedMin = min((solver(rMin, koMin, False), solver(rMin, koMax, False),
                     solver(rMax, koMin, False), solver(rMax, koMax, False)))
    solvedMax = max((solver(rMin, koMin, True),  solver(rMin, koMax, True),
                     solver(rMax, koMin, True),  solver(rMax, koMax, True)))
    solvedMin = max((solvedMin, tsoMin))
    solvedMax = min((solvedMax, tsoMax))
    assert(solvedMin <= solvedMax)
    return [solvedMin, solvedMax]

# Solvers for first operand (o1), given known result (r) and second operand
# (o1).  Pass 'True' for 'maxP' if looking for a maximum value and 'False' if
# looking for a minimum value.
firstOperandSolvers = {
    'inp' : lambda r, o2, maxP: 9 if maxP else 1,
    'add' : lambda r, o2, maxP: r - o2,
    'mul' : lambda r, o2, maxP: solveForMultiplicand(r, o2, maxP),
    'div' : lambda r, o2, maxP: solveForNumerator(r, o2, maxP),
    'mod' : lambda r, o2, maxP: INTMAX if maxP else r,
    'eql' : lambda r, o2, maxP: o2 if r else INTMAX if maxP else INTMIN,
    'not' : lambda r, o2, maxP: not r
}

secondOperandSolvers = {
    'inp' : None,
    'add' : lambda r, o1, maxP: r - o1,
    'mul' : lambda r, o1, maxP: solveForMultiplicand(r, o1, maxP),
    'div' : lambda r, o1, maxP: solveForDenominator(r, o1, maxP),
    'mod' : lambda r, o1, maxP: INTMAX if maxP else r if o1 == r else o1+r,
    'eql' : lambda r, o1, maxP: o1 if r else INTMAX if maxP else INTMIN,
    'not' : None
}

inputRanges = [None] + [[1, 9]] * 14
def rangeSolve(operation, oldResultRange):
    """Recursively solve the values for operation, narrowing the range to
    specified new range in 'operation'"""
    opcode, resultRange, operand1, operand2 = (operation + (None,))[:4]

    if resultRange == oldResultRange:
        return

    if opcode == 'inp':
        assert(isinstance(operand1, int))
        print(f'inp {operand1} = {resultRange}')
        inputRanges[operand1] = resultRange
        return

    range1 = getRange(operand1)
    range2 = getRange(operand2) if operand2 != None else [None, None]
    if isinstance(operand1, tuple):
        firstSolver = firstOperandSolvers[opcode]
        oldRange1 = range1.copy()
        range1 = applySolver(resultRange, range2, oldRange1, firstSolver)
    if isinstance(operand2, tuple):
        secondSolver = secondOperandSolvers[opcode]
        oldRange2 = range2.copy()
        range2 = applySolver(resultRange, range1, oldRange2, secondSolver)
    if isinstance(operand1, tuple):
        setRange(operand1, range1)
        rangeSolve(operand1, oldRange1)
    if isinstance(operand2, tuple):
        setRange(operand2, range2)
        rangeSolve(operand2, oldRange2)

def solve(operation, val = 0):
    oldResultRange = operation[1].copy()
    setRange(operation, [val, val])
    rangeSolve(operation, oldResultRange)

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
solve(registers['z'], 0)
#for reg in "wxyz":
#    print(f"depth at {reg} = {depth(registers[reg])}")
#     print(f"reg {reg} = {registers[reg]}")
# print(registers['z'])
