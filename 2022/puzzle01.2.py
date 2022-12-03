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

elfCalories = list()

currElf = 1
currElfCalories = 0

for line in input:
    if line == "\n":  # Empty line
        elfCalories.append(currElfCalories)
        currElf += 1
        currElfCalories = 0
        continue

    currElfCalories += int(line)

elfCalories.append(currElfCalories)

elfCalories.sort(reverse=True)

top3Calories = elfCalories[0] + elfCalories[1] + elfCalories[2]

print(f'Top 3 elves carry {top3Calories} calories')
