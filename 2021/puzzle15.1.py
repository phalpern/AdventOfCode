# Advent of Code day 15, part 1
# Least risky path through cave

import sys

riskLevels = [ ]

# Lowest risk for any path found for a specific grid square
lowestRiskGrid = [ ]

# Read a 2-D array of risk levels, each in the range 0-9 and return the array.
def readRiskLevels(infile):
    for rowStr in infile:
        riskLevels.append(list(map(int, iter(rowStr.rstrip()))))
        lowestRiskGrid.append(list(map(lambda x : sys.maxsize, riskLevels[0])))

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
        self.risk = link.risk + riskLevels[x][y] if link else 0
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
    global workQueue
    global lowestRiskGrid
    # print("advancePath({})".format(path))
    maxX = len(riskLevels) - 1
    maxY = len(riskLevels[0]) - 1
    x = path.x
    y = path.y
    if path.risk < lowestRiskGrid[x][y]:
        lowestRiskGrid[x][y] = path.risk
    else:
        return False  # Stop searching this path; riskier than best path so far
    if x == maxX and y == maxY:
        return True
    for x1, y1 in [ (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1) ]:
        if x1 < 0 or maxX < x1 or y1 < 0 or maxY < y1:
            continue
        else:
            newPath = Path(x1, y1, path)
            workQueue.append(newPath)
    return False

infile = open("puzzle15_input.txt", "r")

readRiskLevels(infile)
infile.close()
# print(riskLevels)

# pathsFound = 0
bestPath = None
workQueue = [ Path(0, 0) ]
while workQueue:
    # Sort work queue so that the least risky path so far will be popped first.
    # That way, we are always exploring the frontier of the least-risky paths.
    workQueue.sort(key = lambda p : p.risk, reverse = True)
    # Depth-first search, descend down one path
    nextPath = workQueue.pop()
    if advancePath(nextPath):
        bestPath = nextPath
        # pathsFound += 1
        # print("\rPaths = {}, risk = {}  ".format(pathsFound, bestPath.risk), end='')
        # print("Found path {}, with risk {}".format(bestPath, bestPath.risk))
        break

print("\nBest path =", bestPath)
print("Lowest risk =", bestPath.risk)
