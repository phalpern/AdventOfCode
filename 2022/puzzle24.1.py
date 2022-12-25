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

# Each cell of the map contains the bitwize AND of one or more of the following
# values.
EMPTY, EXPEDITION, WALL = 0, 1, 2
BLIZZARD_RIGHT, BLIZZARD_DOWN, BLIZZARD_LEFT, BLIZZARD_UP = 4, 8, 16, 32

symToVal = {
    '.' : EMPTY,
    'E' : EXPEDITION,
    '#' : WALL,
    '>' : BLIZZARD_RIGHT,
    'v' : BLIZZARD_DOWN,
    '<' : BLIZZARD_LEFT,
    '^' : BLIZZARD_UP
}

# Create reverse mapping
valToSym = dict()
for sym, val in symToVal.items():
    valToSym[val] = sym
for blizzards in range(BLIZZARD_RIGHT, 2 * BLIZZARD_UP):
    nblizzards = 0
    for b in (BLIZZARD_RIGHT, BLIZZARD_DOWN, BLIZZARD_LEFT, BLIZZARD_UP):
        if blizzards & b: nblizzards += 1
    if nblizzards > 1: valToSym[blizzards] = str(nblizzards)

def printMap(theMap, header = ""):
    """Print a friendly representation of a map represented as a numpy array"""
    print("")
    print(header)
    for row in range(theMap.shape[0]):
        s = "".join(map(lambda x: valToSym[x], theMap[row,:]))
        print(s)

def moveBlizzards(currMap):
    """Given the current map, create a map of the next position of all the
    blizards"""
    # Create a blank map containing only the walls
    nextMap = currMap & WALL
    lastRow = currMap.shape[0] - 2  # Exclude bottom wall
    lastCol = currMap.shape[1] - 2  # Exlcude right wall
    for row in range(1, lastRow + 1):
        for col in range(1, lastCol + 1):
            currCell = currMap[row, col]
            # Note: check all 4 bits (do not use `elif`)
            if currCell & BLIZZARD_RIGHT:
                nextCol = 1 if col == lastCol else col + 1
                nextMap[row, nextCol] |= BLIZZARD_RIGHT
            if currCell & BLIZZARD_DOWN:
                nextRow = 1 if row == lastRow else row + 1
                nextMap[nextRow, col] |= BLIZZARD_DOWN
            if currCell & BLIZZARD_LEFT:
                nextCol = lastCol if col == 1 else col - 1
                nextMap[row, nextCol] |= BLIZZARD_LEFT
            if currCell & BLIZZARD_UP:
                nextRow = lastRow if row == 1 else row - 1
                nextMap[nextRow, col] |= BLIZZARD_UP
    return nextMap

def moveExpedition(currMap, nextMap):
    """Return a map with an expedition bit set in each cell where the
    expedition could be next. The nextMap argument has the next position of
    all of the blizzards and is upated"""
    lastRow = currMap.shape[0] - 1  # Include bottom wall
    lastCol = currMap.shape[1] - 2  # Exlcude right wall
    for row in range(0, lastRow + 1):
        for col in (currMap[row,:] == EXPEDITION).nonzero()[0]:
            # Try each of the 4 directions as well as standing still
            for drow, dcol in ( (0, 0), (0, 1), (1, 0), (0, -1), (-1, 0) ):
                nextRow = row + drow
                nextCol = col + dcol
                if nextRow < 0 or lastRow < nextRow: continue
                if nextMap[nextRow][nextCol] == EMPTY:
                    nextMap[nextRow][nextCol] = EXPEDITION
    return nextMap

# Read map
currMap = None
for line in input:
    nextRow = [ symToVal[x] for x in line.rstrip() ]
    if currMap is None:
        currMap = np.array(nextRow)
    else:
        currMap = np.vstack([ currMap, nextRow ])

# Find entrance in first row and exit in last row of map
entranceCol = np.where(currMap[ 0,:] == EMPTY)[0][0]
exitCol     = np.where(currMap[-1,:] == EMPTY)[0][0]

currMap[0, entranceCol] = EXPEDITION
# printMap(currMap, "Initial State")

numMinutes = 0
while currMap[-1, exitCol] != EXPEDITION:
    numMinutes += 1
    nextMap = moveBlizzards(currMap)
    currMap = moveExpedition(currMap, nextMap)
    # printMap(currMap, f"Minute {numMinutes}")

print(f"Finished in {numMinutes} minutes")
