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
commonDivisor = 1  # Common divisor for all monkeys

def opAdd(a, b):
    return a + b

def opSub(a, b):
    return a - b

def opMult(a, b):
    return a * b

def opDiv(a, b):
    return a // b

def identity(arg):
    return arg

opMap = { '+' : opAdd, '-' : opSub, '*' : opMult, '/' : opDiv }

class Monkey:
    """Represents one monkey's list of items and its behavior"""

    def __init__(self, initialItems, operation, divisibleTest,
                 recipientIfTrue, recipientIfFalse):
        """Initialize a monkey with the specified attributes. Note that
        `operation` is an executable object, such as a lambda or function,
        taking one argument (the item being inspected), and returning the new
        worry level and `divisibleTest` is a number that the new worry level
        needs to be divisibile by to return `True` for the test."""
        self.items            = initialItems
        self.operation        = operation
        self.divisibleTest    = divisibleTest
        self.recipientIfTrue  = recipientIfTrue
        self.recipientIfFalse = recipientIfFalse
        self.itemsInspected   = 0

    def inspectAndThrow(self, monkeys):
        """Inspect the items, compute the new worry level, and throw according
        to the divisible test."""
        while self.items:
            self.itemsInspected += 1
            item = self.items.pop(0)
            item = self.operation(item)
            # Item can be reduced by common divisor of all divisible tests and
            # still follow the same pattern of monkey-to-monkey throws.
            item %= commonDivisor
            if item % self.divisibleTest == 0:
                recipient = self.recipientIfTrue
            else:
                recipient = self.recipientIfFalse
            monkeys[recipient].items.append(item)

class Expr:
    """An executable object that represents the expression, x _op_ y,
    where x and y are either integers or the variable, `old`, and _op_ is one
    of the arithmetic operations: +, -, *, or /. Given an `Expr` object, `f`,
    `f(old)` returns the result of evaluating the expression."""
    placeholder = "old"

    def __init__(self, exprStr):
        """Parse an expression of the form "x _op_ y" and create an executable
        object representing that expression."""
        x,op,y  = exprStr.split()
        assert("+-*/".find(op) >= 0)  # Valid
        self.op = opMap[op]
        self.x  = Expr.placeholder if x == "old" else int(x)
        self.y  = Expr.placeholder if y == "old" else int(y)

    def __call__(self, old):
        """Evaluate this expression on the (integer) value `old` and return the
        result."""
        x = old if self.x is Expr.placeholder else self.x
        y = old if self.y is Expr.placeholder else self.y
        return self.op(x, y)

# Prefixes used for parsing the input
fieldPrefixes = [ "Monkey ",
                  "  Starting items: ",
                  "  Operation: new = ",
                  "  Test: divisible by ",
                  "    If true: throw to monkey ",
                  "    If false: throw to monkey " ]

monkeys = []  # Barrel of monkeys :-)
while True:
    fields = [ ]
    for prefix in fieldPrefixes:
        line = input.readline().rstrip()
        assert(line.startswith(prefix))
        fields.append(line[len(prefix):])

    monkeyNum        = int(fields[0].rstrip(':'))
    startingItems    = [ int(x) for x in fields[1].split(",") ]
    operation        = Expr(fields[2])
    divisibleTest    = int(fields[3])
    recipientIfTrue  = int(fields[4])
    recipientIfFalse = int(fields[5])
    commonDivisor    *= divisibleTest

    assert(monkeyNum == len(monkeys))
    monkey = Monkey(startingItems, operation, divisibleTest,
                    recipientIfTrue, recipientIfFalse)
    monkeys.append(monkey)

    if not input.readline(): break

snapshots = { 1, 20, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000 }
for i in range(10000):
    for monkey in monkeys:
        monkey.inspectAndThrow(monkeys)
    if i + 1 in snapshots:
        print(f"== After round {i + 1} ==")
        for i,monkey in enumerate(monkeys):
            print(f"Monkey {i} inspected items {monkey.itemsInspected} times.")
        print("")

mostActivity       = 0
secondMostActivity = 0
for i,monkey in enumerate(monkeys):
    print(f"Monkey {i}: {monkey.items}")
    if monkey.itemsInspected >= mostActivity:
        secondMostActivity = mostActivity
        mostActivity       = monkey.itemsInspected
    elif monkey.itemsInspected > secondMostActivity:
        secondMostActivity = monkey.itemsInspected

monkeyBusiness = mostActivity * secondMostActivity

print(f"Two most active monkeys inspected {mostActivity} and {secondMostActivity} items, respectively")
print(f"Monkey business = {monkeyBusiness}")
