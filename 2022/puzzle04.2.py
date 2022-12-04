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
import re

input = openInput.openInput(sys.argv)

overlaps = 0
lineparse = re.compile(r'([0-9]*)-([0-9]*),([0-9]*)-([0-9]*)')
for line in input:
    match = lineparse.match(line)
    range1start = int(match[1])
    range1end   = int(match[2])
    range2start = int(match[3])
    range2end   = int(match[4])
    if range1start <= range2start and range2start <= range1end:
        overlaps += 1
    elif range2start <= range1start and range1start <= range2end:
        overlaps += 1

print(f"Total overlaps = {overlaps}")
