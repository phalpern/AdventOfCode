# Advent of Code day 15, part 1
# Least risky path through tiled cave

import sys

tile = [ ]
tileRows = 1
tileCols = 1
caveRows = 0
caveCols = 0

# Lowest known risk for any path found for a specific grid square
lowestKnownRisk = [ ]

# Return risk for cave cell (x, y)
def getRisk(x, y):
    risk = tile[x % tileRows][y % tileCols]
    risk += int(x / tileRows) + int(y / tileCols)
    return (risk - 1) % 9 + 1

# Read a 2-D array of risk levels, each in the range 0-9 and return the array.
def readRiskLevels(infile):
    global tileRows, tileCols, caveRows, caveCols, tile, lowestKnownRisk
    for rowStr in infile:
        tile.append(list(map(int, iter(rowStr.rstrip()))))
    tileRows = len(tile)
    tileCols = len(tile[0])
    caveRows = tileRows * 5
    caveCols = tileCols * 5
    # Fill `lowestKnownRisk` with `sys.maxsize` values.
    maxsizeRow = list(map(lambda x : sys.maxsize, range(caveCols)))
    lowestKnownRisk = list(map(lambda x : maxsizeRow.copy(), range(caveRows)))
    assert(len(lowestKnownRisk) == caveRows)
    assert(len(lowestKnownRisk[0]) == caveCols)

# Representation of a path (or partial path) through the cave along with the
# risk so far.
class Path:
    # Representation is a linked list from the end of the path to the beginning.
    x     : 0    # x coordinate of last cell in path
    y     : 0    # y coordinate of last cell in path
    risk  : 0    # Total risk of path so far
    link  : None # Link to rest of path

    # Iterate (in reverse order) over the values in the path
    class Iterator:

        path : None

        def __init__(self, path):
            self.path = path

        def __iter__(self):
            return self

        def __next__(self):
            if self.path == None:
                raise StopIteration
            else:
                coord = self.path.lastCoord()
                self.path = self.path.link
                return coord

    def __init__(self, x, y, link=None):
        self.x    = x
        self.y    = y
        self.risk = link.risk + getRisk(x, y) if link else 0
        self.link = link

    def __iter__(self):
        return Path.Iterator(self)

    # Represent the path as a list (in forward order) of coordinates
    def __repr__(self):
        return str(list(reversed(list(iter(self)))))

    # Return `True` if `(x, y)` exists in this path; else `False`
    def hasCoord(self, x, y):
        for c in self:
            if c == (x, y):
                return True
        return False

    # Return the last coordinate in the path
    def lastCoord(self):
        return (self.x, self.y)

# List of paths to be explored. The main loop will pop the least-risky path off
# this queue and traverse another level.
workQueue = [ ]

# If path leads to the exit cell, then stop and return True.
# Otherwise, push all possible next steps onto `workQueue`
def advancePath(path):
    # print("advancePath({})".format(path))
    global lowestKnownRisk
    x = path.x
    y = path.y
    if path.risk < lowestKnownRisk[x][y]:
        lowestKnownRisk[x][y] = path.risk
    else:
        return False  # Stop searching this path; riskier than best path so far
    if x == caveRows - 1 and y == caveCols - 1:
        return True
    for x1, y1 in [ (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1) ]:
        if x1 < 0 or caveRows <= x1 or y1 < 0 or caveCols <= y1:
            continue
        else:
            newPath = Path(x1, y1, path)
            workQueue.append(newPath)
    return False

infile = open("puzzle15_input.txt", "r")
readRiskLevels(infile)
infile.close()
# print(tile)

print("caveRows = {}, caveCols = {}".format(caveRows, caveCols))

# pathsFound = 0
bestPath = None
workQueue = [ Path(0, 0) ]
oldFrontier = (0, 0)
while workQueue:
    # Sort work queue so that the least risky path so far will be popped first.
    # That way, we are always exploring the frontier of the least-risky paths.
    workQueue.sort(key = lambda p : p.risk, reverse = True)
    # Depth-first search, descend down one path
    nextPath = workQueue.pop()
    if nextPath.x + nextPath.y > oldFrontier[0] + oldFrontier[1]:
        # Display progress when the New York distance from origin increases
        print("\rFrontier = ({}, {})      ".format(nextPath.x, nextPath.y), end='')
        oldFrontier = (nextPath.x, nextPath.y)
    if advancePath(nextPath):
        bestPath = nextPath
        # pathsFound += 1
        # print("\rPaths = {}, risk = {}  ".format(pathsFound, bestPath.risk), end='')
        # print("Found path {}, with risk {}".format(bestPath, bestPath.risk))
        break

print("\nBest path =", bestPath)
print("Lowest risk =", bestPath.risk)
