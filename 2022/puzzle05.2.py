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
import re

input = openInput.openInput(sys.argv)

# `stacks` is a list of lists.  Each list is one stack, indexed from 1
# (`stacks[0]` is not used).  Each stack is a list of letters, each
# representing a crate.
stacks = [None]

for line in input:
    if line[1] == '1':
        # Found stack indexes. Verify that we read the right number of stacks.
        assert(len(stacks) - 1 == int(line[-4:]))
        break

    # the form "[X] [Y] [Z]", where a crate ID appears at every 4th position,
    # starting at 1 (but where some positions are blank).
    i = 0
    for p in range(1, len(line) - 1, 4):
        i += 1
        crate = line[p]
        if i >= len(stacks): stacks.append([])
        if crate != ' ':     stacks[i].insert(0, crate)

# Skip blank line
blankLine = next(input)
assert(blankLine == '\n')

# Each line from here on out is in the form "move N from X to Y", where N is
# the number of crates to move and X and Y are stack indexes.
pattern = re.compile(r'move ([0-9]*) from ([0-9]*) to ([0-9]*)')
for line in input:
    match = pattern.match(line)
    assert(match)
    N = int(match[1])
    X = int(match[2])
    Y = int(match[3])
    stacks[Y] += stacks[X][-N:]
    stacks[X] =  stacks[X][:-N]

result = ""
for stack in stacks:
    if stack is None: continue
    print(stack)
    result += stack[-1]

print(f'Result = "{result}"')
