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
import functools

input = openInput.openInput(sys.argv)

class RereadIter:
    """Iterator to traverse an iterator, enabling re-reading of the
    most-recently visited item.
    """
    def __init__(self, iterable):
        """Initialize from an iterator"""
        self.iterable  = iter(iterable)
        self.lastItem  = None  # Most-recently read item

    def __iter__(self):
        return self

    def __next__(self):
        """Return the next item or throw StopIteration"""
        self.lastItem = next(self.iterable)
        return self.lastItem

    def current(self):
        """Return the item most recently returned by `__next__`."""
        return self.lastItem

def skipWhitespace(iterator):
    """Advance `iterator` to consume zero or more space characters.
    If `iterator.current()` is not a space, does nothing.

    Postcondition: iterator.current() is the first character after the spaces
    Returns:       next character after last whitespace character
    """
    c = iterator.current()
    while c == ' ':            # Consume 0 or more spaces
        c == next(iterator)
    return iterator.current()

def skipCommaAndWhitespace(iterator):
    """Advance `iterator` to consume zero or one comma surrounded by zero or more
    whitespace characters. If `iterator.current()` is not a space or comma,
    does nothing.

    Postcondition: iterator.current() is the first character after the spaces
                   and optional comma. At most one comma is consumed.
    Returns:       next character after last comma or whitespace character
    """
    c = skipWhitespace(iterator)
    if c == ',':
        c == next(iterator)  # Consume the comma
    return skipWhitespace(iterator)

def parseInt(iterator):
    """Parse and return the integer at iterator.

    Precondition:  iterator.current() is a digit
    Postcondition: iterator.current() is the first character after the integer
    Returns:       the integer value (of type `int`)
    """
    intStr = ""
    c = iterator.current()
    assert(c.isdigit())
    while c.isdigit():
        intStr += c
        c = next(iterator)
    return int(intStr)

def parseList(iterator):
    """Parse and return the list at iterator.

    Precondition:  iterator.current() is '['
    Postcondition: iterator.current() is the first character after the list
    Returns:       the list value (of type `list`)
    """
    theList = [ ]
    assert('[' == iterator.current())
    next(iterator)
    c = skipWhitespace(iterator)
    while c != ']':
        if c == '[':
            item = parseList(iterator)
        elif c.isdigit():
            item = parseInt(iterator)
        else:
            assert(False)
        theList.append(item)
        c = skipCommaAndWhitespace(iterator)
    assert(c == ']')
    next(iterator)
    return theList

def compare(item1, item2):
    """Return -1 if, lexicographically, item1 comes before item2, 0 if they are
    equivalent, and 1 if item2 comes before item 1"""
    if isinstance(item1, int) and isinstance(item2, int):
        if item1 < item2: return -1
        if item2 < item1: return  1
        return 0
    elif isinstance(item1, list) and isinstance(item2, list):
        for i, subitem1 in enumerate(item1):
            if len(item2) <= i: return 1  # item2 is out of subitems
            c = compare(subitem1, item2[i])
            if c != 0: return c
        if len(item1) < len(item2): return -1
        return 0
    elif isinstance(item1, int):
        return compare([ item1 ], item2)
    else:
        return compare(item1, [ item2 ])

packets = []
pairIndex = 0
sum = 0
for line in input:
    if line == '\n': continue
    iterator = RereadIter(line)
    next(iterator)
    packets.append(parseList(iterator))

packets += [ [[2]], [[6]] ]  # Dividers
packets = sorted(packets, key=functools.cmp_to_key(compare))
# for packet in packets:
#     print(packet)

sepIndex1 = packets.index([[2]]) + 1
sepIndex2 = packets.index([[6]]) + 1
decoderKey = sepIndex1 * sepIndex2

print(f"Decoder key = {decoderKey}")
