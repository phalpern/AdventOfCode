#! /usr/bin/python3

# Usage: puzzleXX.Y.py [input-suffix]
#
# Where XX is the puzzle number in decimal (with leading zero, if necessary)
# and Y is the sub-part (1 or 2).  By default, the input-suffix is "input", so
# the input file would be puzzle "puzzleXX_input.txt".  Note that the input to
# the two parts of one puzzle is typically the same file, so Y does not show up
# in the default input file name.

import sys
import re

# BOILERPLATE TO FIND AND OPEN INPUT FILE
puzzle = re.sub(r'\.[^/]*$', "", sys.argv[0])
if len(sys.argv) > 1:
    inputFilename = puzzle + '_' + sys.argv[1] + ".txt"
else:
    inputFilename = puzzle + "_input.txt"

input = open(inputFilename, "r"); # Input sequence, one number per line
print(f"Reading input from {inputFilename}...")
# END BOILERPlATE

def priority(items):
    """Returns the some of the prioritities of specified `items`"""
    setPriority = 0
    for item in items:
        itemVal = ord(item)
        if itemVal >= ord('a'):
            priority = 1 + itemVal - ord('a')
            assert(1 <= priority and priority <= 26)
        else:
            priority = 27 + itemVal - ord('A')
            assert(27 <= priority and priority <= 52)
        setPriority += priority
        return setPriority

totalBadgePriority = 0
elfIndex = 0
groupSacks = [ "", "", "" ]
for line in input:
    groupSacks[elfIndex] = set(line.rstrip('\n'))
    if elfIndex == 2:
        intersection = groupSacks[0].intersection(groupSacks[1]).intersection(groupSacks[2])
        assert(1 == len(intersection))
        totalBadgePriority += priority(intersection)
        elfIndex = 0
    else:
        elfIndex += 1

print(f"Total badge priority = {totalBadgePriority}")
