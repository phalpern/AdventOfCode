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

def findVisible(treegridSlice, visibilitySlice):
    """For each visible tree in `treegridSlice`, set the corresponding element of
    `visibilitySlice` to `True`. The `treegridSlice` array is a 1-d slice of the
    tree grid, where the first and last elements are on the edge of the grid
    and the remaining elements may or may not be on the edge. `visibilitySlice`
    is the corresponding slice of the visibility grid.
    """
    maxHeight      = -1
    # Traverse in forward direction
    for i in range(len(treegridSlice)):
        if treegridSlice[i] > maxHeight:
            visibilitySlice[i] = True
            maxHeight = treegridSlice[i]
    # Traverse in reverse direction
    maxHeightRev = -1
    for i in range(len(treegridSlice)-1, -1, -1):
        if treegridSlice[i] > maxHeightRev:
            visibilitySlice[i] = True
            maxHeightRev = treegridSlice[i]
        if maxHeightRev == maxHeight:
            break

# Bit array with a True for each visible tree
visibilityGrid = np.zeros(grid.shape, bool)

# Traverse each row, then each column
for row in range(nrows):
    findVisible(grid[row,:], visibilityGrid[row,:])

for col in range(ncols):
    findVisible(grid[:,col], visibilityGrid[:,col])

print(visibilityGrid)
total = np.sum(visibilityGrid)
print(f"Num visible trees = {total}")
