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
import numpy as np

input = openInput.openInput(sys.argv)

air, rock, sand = (0, 1, 2)
caveSymbols = ".#o"

def printCave(cave):
    """Print the cave layout, where `cave` is a 2-d array filled with values
    `air`, `rock`, and `sand`"""
    for row in range(cave.shape[0]):
        print("{0:>3} {1}".
              format(row, ''.join([ caveSymbols[v] for v in cave[row,:] ])))

# The rock wall is a list of rock lines.  Each rock line consists of a
# 4-element tuple, (x1, y1, x2, y2), where (x1, y1) is the starting point and
# (x2, y2) is the end point, inclusive.
rockLines = [ ]

# Sand comes int at point (500, 0)
sandEntrance = (500, 0)

# Boundaries of the space
minx, miny = sandEntrance
maxx, maxy = sandEntrance

# Sand originating from a specific point forms a cone, spreading diagnally down
# and to the left and right. The horizontal spread in each direction is equal
# to the vertical distance to the floor from the origination point.  As each
# rock outcropping is discovered, it becomes a new origination point if it is
# farther to the left or right than the natural spread of the cone of sand
# above it.  The following variables keep track of the leftmost and rightmost
# cones of sand.
leftConey  = miny
rightConey = miny

for line in input:
    line = line.rstrip()
    pointStrings = line.split(" -> ")
    x1, y1, x2, y2 = (None, None, None, None)
    for pointString in pointStrings:
        (x1, y1) = (x2, y2)
        (x2, y2) = [ int(v) for v in pointString.split(',') ]
        miny = min(miny, y2)
        maxy = max(maxy, y2)
        minx -= maxy - leftConey  # Account for additional left spread, if any
        leftConey = maxy
        maxx += maxy - rightConey # Account for additional right spread, if any
        rightConey = maxy
        spread = maxy - y2  # How wide would a code from here spread
        minx = min(minx, x2 - spread)
        maxx = max(maxx, x2 + spread)
        if x1 is None: continue
        rockLines.append((x1, y1, x2, y2))

maxy += 2  # Add 2 vertical units from miny to floor
nrows = maxy - miny + 1
# Sand spreads diagnally to the left and right from the leftmost and rightmost
# rock outcroppings, respectively.  The amount of horizonal spread is equal to
# the vertical distance from the outcropping to the floor.
minx -= maxy - leftConey   # Spread to the left from leftmost rock
maxx += maxy - rightConey  # Spread to the right from rightmost rock
ncols = maxx - minx + 1

cave = np.full([nrows, ncols], air)  # Fill with air
cave[-1,:] = np.full((ncols), rock)  # Create floor of rock

for x1, y1, x2, y2 in rockLines:
    if x1 == x2:
        if y1 > y2: y1, y2 = y2, y1   # y1 should be less or equal to than y2
        for y in range(y1, y2 + 1):
            cave[y - miny, x1 - minx] = rock
    else:
        assert(y1 == y2)  # Line must be vertical or horizontal, not diagonal
        if x1 > x2: x1, x2 = x2, x1   # x1 should be less or equal to than x2
        for x in range(x1, x2 + 1):
            cave[y1 - miny, x - minx] = rock

# Process sand entering at `sandEntrance`. Since `cave` is offset so that
# location `(minx, miny)` is at `(0, 0)`, we similarly comput the offset column
# (x axis) and row (y axis) for `sandEntrance`.
sandEntranceCol = sandEntrance[0] - minx
sandEntranceRow = sandEntrance[1] - miny
sandUnits = 0
done = False
while not done:
    # Process one unit of sand entering at `sandEntrance`
    if cave[sandEntranceRow, sandEntranceCol] != air:
        done = True
        break  # No room for more sand

    # Trace path of sand unit downwards until the unit comes to rest.
    # `IndexError` is raised if the sand falls off the sides or bottom of
    # the cave, indicating that no more sand can come to a rest.
    col = sandEntranceCol
    for row in range(sandEntranceRow, nrows + 2):
        if cave[row, col] == air:
            pass
        elif cave[row, col - 1] == air:
            col -= 1
        elif cave[row, col + 1] == air:
            col += 1
        else:
            cave[row - 1, col] = sand  # Unit came to on previous row
            sandUnits += 1
            break

printCave(cave)
print(f"Number of units = {sandUnits}")
