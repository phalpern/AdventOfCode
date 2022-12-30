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

# # Design:
#
# The input is an irregularly shaped grid representing the six faces of a
# flattened cube.  Representing the cube and navigating its surfaces present
# the following challenges and design solutions:
#
# ## Terminology
#
# We refer to the sides of our cube as the *front*, *back*, *right*, *left*,
# *top*, and *bottom*.
#
# We refer to the direction of motion on one 2-D face of the cube as *right*,
# *left*, *up*, and *down*.
#
# We refer to a change in direction (per commands in the specified path) as
# *turning right* or *turning left*.
#
# Note that *right* and *left* are used in three different ways: to label the
# side of the cube, to describe a direction, and to describe a change of
# direction. To avoid confusion, we will try, whenever there is possible
# ambiguity (especially in the names of program constants) to use a
# disambiguating term as in "right face", "move right", or "turn right".
#
# A *panel* is a 2-D square grid of '.' and '#' symbols that is mapped to one
# face of the cube. There are six panels described in the input stream.
#
# The *orientation* of a panel on a cube face is the mapping from the input
# coordinate system to 3-D cube coordinate system.  It is described, in our
# design, by mapping each side of the 2-D panel to the adjacent face of the
# cube. For example, if a panel, *P* is mapped to the right face, it can be
# oriented such that the top row of *P* is adjacent to either the front,
# top, back, or bottom side of the cube.
#
#
# ## Detecting the size of the cube from the input
#
# The input consists of a series of lines containing the symbols '.' and '#'
# (for open tiles and wall tiles, respectively), grouped into 6 square panels
# arranged in an irregular shape that defines a flattened cube. Some rows have
# leading spaces, i.e., when the panel is not left-most in the flattened
# shape. The main challenge in determining the size of the cube is that there
# are no delimiters between horizontally adjacent panels, so the width of one
# panel cannot be determined without more context.
#
# The solution chosen here is to read all of the input at once, sum up the
# count of non-space characters of all the lines, divide that by 6 (to find the
# number of tiles in each panel) and find its square root to get the length of
# each side.
#
#
# ## Folding the input into a cube
#
# We start with the *origin* panel, which contains the first non-space line in
# the left-to-right, top-to-bottom reading of the input file.  We map the
# origin panel to the **front** of the cube. Then, traversing the panel
# adjacencies from the input, we map each new panel to a face. For example, if
# there is an adjacent panel, *P*, *below* the origin, we map *P* to the bottom
# face and set its orientation so that *up* points to the *front* face.
#
# The formula for determining orientation is as follows:
#
#  1. Determine what face we came from (e.g., the **front** face, in the
#     preceding example)
#  2. Map that face to the direction opposite the direction of traversal (e.g.,
#     in the previous example we are traversing **down** so we map the
#     **front** face to the **up** direction)
#  3. In theory, orientation can be represented as a single mapping of one side
#     of the panel to one face of the cube, but it is convenient to compute the
#     other three sides once the first is determined.
#
# Note that **traversing** the panel adjacencies in the input is different from
# **navigating** from one panel to the next when following the path -- in the
# former case, the orientation of the new panel is determined by the traversal,
# in the latter case, the orientation is already set and can be quite
# different, i.e., when the two panels in question are *not adjacent* in the
# input but *end up adjacent* in the folded cube.
#
#
# ## Navigating the cube
#
# A navigation command is either an integer, indicating the number of steps to
# take in the current direction, or a turn instructoin ('R' or 'L') indicating
# a change in direction.  In the former case, if moving results in navigating
# off the edge of the current panel, then we must determine
#
#  1. which panel we moved to and
#  2. the landing position and relative direction of motion on the new panel.
#
# The new panel is a straightforward to determine: simply look up the panel
# corresponding to the face onto which we've navigated.
#
# The landing position is determined by looking up the edge corresponding to
# the face we **came from** and mapping the linear position appropriately. The
# new logical direction is away from the face we came from.

# Cube faces
FACE_FRONT, FACE_BACK, FACE_RIGHT, FACE_LEFT, FACE_TOP, FACE_BOTTOM = (
    0, 1, 2, 3, 4, 5)

# Directions.  Note that adding one modulo 4 turns right and subtracting 1
# modulo 4 turns left.
MOVE_RIGHT, MOVE_DOWN, MOVE_LEFT, MOVE_UP = 0, 1, 2, 3

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
row, col, direction = 0, 0, MOVE_RIGHT

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
