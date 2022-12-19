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

input = openInput.openInput(sys.argv)

# Set of 1x1x1 cubes at positions (x, y, z)
cubes = set()
for line in input:
    coord = tuple( map(lambda x : int(x), line.split(',')) )
    cubes.add(coord)

numExposedFaces = 0
for x, y, z in cubes:
    # Add 6 new faces, but remove those that are adjacent to another cube
    numExposedFaces += 6
    if (x - 1, y, z) in cubes: numExposedFaces -= 1
    if (x + 1, y, z) in cubes: numExposedFaces -= 1
    if (x, y - 1, z) in cubes: numExposedFaces -= 1
    if (x, y + 1, z) in cubes: numExposedFaces -= 1
    if (x, y, z - 1) in cubes: numExposedFaces -= 1
    if (x, y, z + 1) in cubes: numExposedFaces -= 1

print(f"Number of exposed faces = {numExposedFaces}")
