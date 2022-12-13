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

def getElem(grid, indexTuple):
    """Return the item of the np.array `grid` indexed by two elements of
    `indexTuple`"""
    x, y = indexTuple
    return grid[x, y]

def setElem(grid, indexTuple, val):
    """Set and return the item of the np.array `grid` indexed by two elements of
    `indexTuple` to the value `val`"""
    x, y = indexTuple
    grid[x, y] = val
    return val

def reverseMove(point, offset, grid):
    """Return `point` offset by `offset`, where both `point` and `offset` are numpy
    arrays of length 2. Returns `None` if move is not the reverse of a valid move.
    """
    result = point + offset
    # Fail if out of bounds
    if (result < (0, 0)).any() or (grid.shape <= result).any(): return None
    # Fail if forward move would gain more than 1 in altitude.
    if getElem(grid, point) - getElem(grid, result) > 1: return None
    return result

def findBestStart(target, grid):
    """Find the shortest path from any zero-level square to `target` within `grid`
    and return the number of steps."""
    maxDepth  = grid.shape[0] * grid.shape[1] + 1 # Larger than any optimal path
    minDepths = np.full(grid.shape, maxDepth)     # Shortest seen path to each square
    workQueue = [ ((target,), 0) ]                # Work backwards from target

    # Breadth-first traversal of paths
    while workQueue:
        item  = workQueue.pop(0)
        path  = item[0]
        depth = item[1]
        pos   = path[0]
        if depth >= maxDepth: continue
        if depth >= getElem(minDepths, pos): continue
        setElem(minDepths, pos, depth)
        if getElem(grid, pos) == 0:  # Found a valid path
            maxDepth = depth         # Any path longer than this should be ignored
            continue
        for direction in ((0, -1), (0, 1), (-1, 0), (1, 0)):
            newpos = reverseMove(pos, direction, grid)
            if newpos is None: continue
            workQueue.append(((newpos, path), depth + 1))
    return maxDepth

grid = None
for line in input:
    line = line.rstrip()
    row = [ ord(c) - ord('a') for c in line ]  # Row of values 0 to 25
    if grid is None:
        grid = np.array([ row ])
    else:
        grid = np.append(grid, [ row ], 0)
    S = line.find('S')
    if S >= 0:
        start = coord( grid.shape[0] - 1, S )
        setElem(grid, start, 0)
    E = line.find('E')
    if E >= 0:
        target = coord( grid.shape[0] - 1, E )
        setElem(grid, target, 25)

steps = findBestStart(target, grid)

print(f"Result = {steps}")
