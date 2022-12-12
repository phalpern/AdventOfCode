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
            item //= 3
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
        self.x  = Expr.placeholder if x == "old" else int(x)
        self.y  = Expr.placeholder if y == "old" else int(y)
        self.op = op

    def __call__(self, old):
        """Evaluate this expression on the (integer) value `old` and return the
        result."""
        x = old if self.x is Expr.placeholder else self.x
        y = old if self.y is Expr.placeholder else self.y
        op = self.op
        if op == '+':
            return x + y
        elif op == '-':
            return x - y
        elif op == '*':
            return x * y
        elif op == '/':
            return x // y
        else:
            assert(False)

fieldPrefixes = [ "Monkey ",
                  "  Starting items: ",
                  "  Operation: new = ",
                  "  Test: divisible by ",
                  "    If true: throw to monkey ",
                  "    If false: throw to monkey " ]

monkeys = []
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

    assert(monkeyNum == len(monkeys))
    monkey = Monkey(startingItems, operation, divisibleTest,
                    recipientIfTrue, recipientIfFalse)
    monkeys.append(monkey)

    if not input.readline(): break

for i in range(20):
    for monkey in monkeys:
        monkey.inspectAndThrow(monkeys)

for i,monkey in enumerate(monkeys):
    print(f"Monkey {i}: {monkey.items}")

mostActivity       = 0
secondMostActivity = 0
for i,monkey in enumerate(monkeys):
    print(f"Monkey {i} inspected items {monkey.itemsInspected} times.")
    if monkey.itemsInspected >= mostActivity:
        secondMostActivity = mostActivity
        mostActivity       = monkey.itemsInspected
    elif monkey.itemsInspected > secondMostActivity:
        secondMostActivity = monkey.itemsInspected

monkeyBusiness = mostActivity * secondMostActivity

print(f"Two most active monkeys inspected {mostActivity} and {secondMostActivity} items, respectively")
print(f"Monkey business = {monkeyBusiness}")
