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

# Directions.  Note that adding one modulo 4 turns right and subtracting 1
# modulo 4 turns left.
RIGHT, DOWN, LEFT, UP = 0, 1, 2, 3

# Array of 4 tuples corresponding to the four directions
MOVE_LOOKUP = ((0, 1), (1, 0), (0, -1), (-1, 0))

def move(board, row, col, direction, num):
    """Move 'num' tiles in the specified 'direction' and return the new row and
    column"""
    drow, dcol = MOVE_LOOKUP[direction]
    for i in range(num):
        # Find next row. If reached end of (non-space) tiles, wrap and
        # keep advancing until find next tile.
        nextRow = (row + drow) % len(board)
        while col >= len(board[nextRow]) or board[nextRow][col] == ' ':
            nextRow = (nextRow + drow) % len(board)
        rowString = board[nextRow]

        # Find next column. If reached end of (non-space) tiles, wrap and
        # keep advancing until find next tile.
        nextCol = (col + dcol) % len(rowString)
        while rowString[nextCol] == ' ':
            nextCol = (nextCol + dcol) % len(rowString)

        if board[nextRow][nextCol] == '#':
            break  # Hit a wall; end loop without advancing
        else:
            row, col = nextRow, nextCol  # Advance to next tile

    assert(board[row][col] == '.')
    return row, col


input = openInput.openInput(sys.argv)

board = [ line.rstrip() for line in input ]
path = board.pop()  # Last line of input
board.pop()         # Discard blank line at end

# Direction is 'R', 'L', 'D' or 'U' for Right, Left, Down, or Up
row, col, direction = 0, 0, RIGHT

# Find first column that is not '#' or space
col = board[row].index('.')
print(f"Start row, col = {row}, {col}")

numToMove = 0
for c in path:
    if c.isdigit():
        numToMove *= 10
        numToMove += int(c)
    else:
        row, col = move(board, row, col, direction, numToMove)
        turn = 1 if c == 'R' else -1
        direction = (direction + turn) % 4
        numToMove = 0

# Make final move
row, col = move(board, row, col, direction, numToMove)

password = (row + 1) * 1000 + (col + 1) * 4 + direction
print(f"password is {password}")
