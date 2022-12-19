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

maxx, maxy, maxz = (0, 0, 0)

# list of 1x1x1 cubes at positions (x, y, z)
cubes = [ ]
for line in input:
    x, y, z = tuple( map(lambda x : int(x), line.split(',')) )
    maxx = max(maxx, x)
    maxy = max(maxy, y)
    maxz = max(maxz, z)
    cubes.append((x, y, z))


air        = 0  # Air whose trapped status is unknown
trappedAir = 1  # Air that is known to be trapped
openAir    = 2  # Air that is known not to be trapped
lava       = 3  # Lave cube

# Create an array for the space, filled with air
space = np.full((maxx + 1, maxy + 1, maxz + 1), air)

# Set the lava cubes within the space
for x, y, z in cubes:
    space[x, y, z] = lava

def cellType(space, x, y, z):
    """For a cell at `space[x, y, z]`, determine whether the cell contains trapped
    air, open air, or lava.  For air cells, recursively check adjacent air
    cells until the entire air pocket is determined to be trapped air or open
    air."""
    if (0 <= x and x < space.shape[0] and
        0 <= y and y < space.shape[1] and
        0 <= z and z < space.shape[2] ):
        if space[x, y, z] != air:
            return space[x, y, z]
    else:
        return openAir  # Out-of-bounds cell is always open air

    workQueue = [ (x, y, z) ]
    pocket = { (x, y, z) }   # Set of cells in this pocket of air

    result = None
    while workQueue and result is None:
        x, y, z = workQueue.pop()
        # Check all adjacent cells
        for dx, dy, dz in [ (-1,  0,  0), ( 1,  0,  0),
                            ( 0, -1,  0), ( 0,  1,  0),
                            ( 0,  0, -1), ( 0,  0,  1) ]:
            ax, ay, az = x + dx, y + dy, z + dz
            if (0 <= ax and ax < space.shape[0] and
                0 <= ay and ay < space.shape[1] and
                0 <= az and az < space.shape[2] ):
                adjacent = space[ax, ay, az]
            else:
                adjacent = openAir

            if adjacent == lava:
                pass
            elif adjacent == air:
                if not (ax, ay, az) in pocket:
                    pocket.add((ax, ay, az))
                    workQueue.append((ax, ay, az))
            else:
                result = adjacent
                break

    if result is None: result = trappedAir

    for x, y, z in pocket:
        space[x, y, z] = result

    return result

numExposedFaces = 0
for x, y, z in cubes:
    # Count faces that are exposed to open air
    if cellType(space, x - 1, y, z) == openAir: numExposedFaces += 1
    if cellType(space, x + 1, y, z) == openAir: numExposedFaces += 1
    if cellType(space, x, y - 1, z) == openAir: numExposedFaces += 1
    if cellType(space, x, y + 1, z) == openAir: numExposedFaces += 1
    if cellType(space, x, y, z - 1) == openAir: numExposedFaces += 1
    if cellType(space, x, y, z + 1) == openAir: numExposedFaces += 1

print(f"Number of exposed faces = {numExposedFaces}")
