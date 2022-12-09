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

grid = None
for line in input:
    line = line.rstrip()
    row = [ int(x) for x in line ]
    if grid is None:
        grid = np.array([ row ])
    else:
        grid = np.append(grid, [ row ], 0)

nrows = grid.shape[1]
ncols = grid.shape[0]

print(f"{nrows} rows, {ncols} columns")
print(grid)

def viewingDistance(vector):
    """Compute the viewing distance along the specified `vector`, where the first
    element of `vector` is the tree under consideration and each successive
    element is a tree farther away along one of the cardinal compass directions
    (it doesn't matter which)"""
    heightLimit = vector[0]
    distance  = 0
    for i in range(1, len(vector)):
        if vector[i] >= heightLimit:
            return i
    return len(vector) - 1

highestScore = 0
for i in range(0, nrows):
    for j in range(0, ncols):
        score =  viewingDistance(grid[i, j::-1])  # left
        score *= viewingDistance(grid[i, j:])     # right
        score *= viewingDistance(grid[i::-1, j])  # up
        score *= viewingDistance(grid[i:, j])     # down
        highestScore = max(score, highestScore)

print(f"Highest score = {highestScore}")
