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

    def __init__(self, exprStr):
        """Parse an expression of the form "x _op_ y" and create an executable
        object representing that expression."""
        x,op,y  = exprStr.split()
        assert("+-*/".find(op) >= 0)  # Valid

        # x and y will be a single-item list or tuple.  The reason for this
        # indirection is so that all references to the (mutable) list,
        # `self.old`, will see any changes to the value `self.old[0]`. Thus, I
        # am simulating pointers in Python.
        self.old = [ None ]  # Mutations to `self.old` are visible to all references
        if x == "old":
            x = self.old     # The first operand will be bound to variable, `old`
        else:
            x = ( int(x), )  # The first operand will be bound to an int constant

        if y == "old":
            y = self.old     # The second operand will be bound to variable, `old`
        else:
            y = ( int(y), )  # The second operand will be bound to an int constant

        # Create a lambda closure that evaluates x[0] op y[0]. If x or y is
        # bound to `self.old`, then the value stored prior to evaluating the
        # lambda will be used in the calculation.
        if op == '+':
            self.op = lambda : x[0] + y[0]
        elif op == '-':
            self.op = lambda : x[0] - y[0]
        elif op == '*':
            self.op = lambda : x[0] * y[0]
        elif op == '/':
            self.op = lambda : x[0] // y[0]
        else:
            assert(False)

    def __call__(self, old):
        """Evaluate this expression on the (integer) value `old` and return the
        result."""
        self.old[0] = old  # Usees of `old[0]` in the `op` lambda will refer to `old`
        return self.op()

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
