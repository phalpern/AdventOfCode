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

def adjustTail(head, tail):
    """Return a new tail position to adjust for the distance between the head
    and tail. The head and tail must not start out separated by more than 2
    spaces in any direction"""
    newTail = tail.copy()
    distances = head - tail
    if abs(distances[0]) == 2:
        newTail += distances // 2
        newTail[1] = head[1]  # Move tail y to match head y
    elif abs(distances[1]) == 2:
        newTail += distances // 2
        newTail[0] = head[0]  # Move tail x to match head x
    return newTail

head = coord(0, 0)
tail = coord(0, 0)
visited = set([tuple(tail)])
for line in input:
    direction, steps = line.split()
    steps = int(steps)
    for i in range(steps):
        head = head + moves[direction]
        tail = adjustTail(head, tail)
        visited.add(tuple(tail))

print(f"Num visited = {len(visited)}")
