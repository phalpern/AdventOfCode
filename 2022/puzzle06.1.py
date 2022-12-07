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

for line in input:
    line = line.rstrip()
    buckets = [ 0 for n in range(0, 26) ]
    n_uniq  = 0
    for i in range(0, len(line)):
        if i > 3:
            c = ord(line[i - 4]) - ord('a')
            if buckets[c] == 1: n_uniq -= 1
            buckets[c] -= 1
            if buckets[c] == 1: n_uniq += 1
        c = ord(line[i]) - ord('a')
        assert(0 <= c and c < 26)
        if buckets[c] == 1: n_uniq -= 1
        buckets[c] += 1
        if buckets[c] == 1: n_uniq += 1
        if n_uniq == 4:
            print(f"first marker ends after character {i + 1}")
            break
