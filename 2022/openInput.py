#! /usr/bin/python3

import re

def openInput(argv):
    """Given a program name of the form *puzzleXX.Y.py*, where XX is the puzzle
    number in decimal (with leading zero, if necessary) and Y is the sub-part
    (1 or 2), open and return a data input file of the form
    *puzzleXX_suffix.txt*. By default, the input-suffix is "input", so the
    input file would be "puzzleXX_input.txt", but if an argument is given in
    argv[1], that is used as the suffix, instead..  Note that the input to the
    two parts of one puzzle is typically the same file, so Y does not show up
    in the default input file name.
    """
    puzzle = re.sub(r'\.[^/]*$', "", argv[0])
    if len(argv) > 1:
        inputFilename = puzzle + '_' + argv[1] + ".txt"
    else:
        inputFilename = puzzle + "_input.txt"
    print(f"Reading input from {inputFilename}...")
    return open(inputFilename, "r")
