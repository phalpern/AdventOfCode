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

def coord(x, y):
    """Return a coordinate, `(x, y)` as a numpy array"""
    return np.array((x, y))

# Map a direction to changes in x and y
moves = { 'L' : coord(-1,  0),
          'R' : coord( 1,  0),
          'U' : coord( 0,  1),
          'D' : coord( 0, -1) }

def printSequence(sequence):
    maxx = 0
    maxy = 0
    minx = 0
    miny = 0
    for rope in sequence:
        for knot in rope:
            maxx = max(maxx, knot[0])
            maxy = max(maxy, knot[1])
            minx = min(minx, knot[0])
            miny = min(miny, knot[1])
    width = maxx - minx + 1
    height = maxy - miny + 1
    print(f"minx = {minx}, miny = {miny}")
    print(f"maxx = {maxx}, maxy = {maxy}")
    print(f"width = {width}, height = {height}")
    print(f"Sequence len = {len(sequence)}")
    for rope in sequence:
        grid = np.full([height, width], 11)
        i = 0
        grid[-miny,-minx] = 10  # Origin
        for knot in rope:
            gx = knot[0] - minx
            gy = knot[1] - miny
            grid[gy, gx] = min(grid[gy, gx], i)
            i += 1
        for x in range(height - 1, -1, -1):
            print("".join(map(lambda i : "H123456789s."[i], grid[x,:])))
        print("")

def adjustKnot(prevKnot, currKnot):
    """Return the new position of currKnot to adjust for the distance between
    it and prevKnot. The two knots must not start out separated by more than 2
    spaces in any direction"""
    newCurrKnot = currKnot.copy()
    distances = prevKnot - currKnot
    if abs(distances[0]) == 2 and abs(distances[1]) == 2:
        newCurrKnot += distances // 2
    elif abs(distances[0]) == 2:
        newCurrKnot[0] += distances[0] // 2
        newCurrKnot[1] = prevKnot[1]            # Move currKnot y to match prevKnot y
        assert((newCurrKnot != currKnot).any())
    elif abs(distances[1]) == 2:
        newCurrKnot[1] += distances[1] // 2
        newCurrKnot[0] = prevKnot[0]
        assert((newCurrKnot != currKnot).any())
    return newCurrKnot

sequence = [ ]
rope = 10 * [ coord(0, 0) ]
visited = set([tuple(rope[-1])])
for line in input:
    direction, steps = line.split()
    steps = int(steps)
    for i in range(steps):
        rope[0] = rope[0] + moves[direction]
        for k in range(1, len(rope)):
            rope[k] = adjustKnot(rope[k-1], rope[k])
        # print(tuple(rope[-1]))
        visited.add(tuple(rope[-1]))
    sequence.append(rope.copy())

# printSequence(sequence)
print(f"Final tail position = {tuple(rope[-1])}")
print(f"Num visited = {len(visited)}")
