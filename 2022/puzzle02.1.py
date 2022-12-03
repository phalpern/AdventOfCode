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

choiceScore = { 'X' : 1, 'Y' : 2, 'Z' : 3 }
roundScore  = { 'AX' : 3, 'AY' : 6, 'AZ' : 0,
                'BX' : 0, 'BY' : 3, 'BZ' : 6,
                'CX' : 6, 'CY' : 0, 'CZ' : 3 }

totalScore = 0
for line in input:
    opponent = line[0]
    me       = line[2]
    play     = opponent + me
    score    = choiceScore[me] + roundScore[play]
    totalScore += score

print(f"Total score = {totalScore}")
