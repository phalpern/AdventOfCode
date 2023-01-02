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
import math

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
# A *panel* is a 2-D square grid of '.' and '#' symbols that is mapped to one
# face of the cube. There are six panels described in the input stream.
#
# We refer to the direction of motion on one panel as *east*, *south*, *west*,
# and *north*. Note that a panel can be mapped to a cube face in any of four
# orientations (see *orientation*, below), so north is not necessarily in the
# direction of the top face of the cube.
#
# We refer to a change in direction (per commands in the input path) as
# *turning right* or *turning left*.
#
# Note that *right* and *left* are used in two different ways: to label the
# side of the cube and to describe a change of direction. To avoid confusion,
# we will try, whenever there is possible ambiguity (especially in the names of
# program constants) to use a disambiguating term as in "right face" or "turn
# right".
#
# The *orientation* of a panel on a cube face is the mapping from the input
# coordinate system to the 3-D cube coordinate system.  It is described, in our
# design, as a mapping from each direction out of the 2-D panel to an adjacent
# face of the cube. For example, if a panel, *P* is mapped to the right face,
# it can be oriented such moving north out of the panel lands you on the front
# face of the cube, or it can be oriented such that nort goes to the top, back,
# or bottom faces of the cube, for a total of four possible orientations.
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

################# CONSTANTS ########################

# Cube face names, in arbitrary order except that `FRONT_FACE` is the face
# where we start navigation.
FRONT_FACE, BACK_FACE, RIGHT_FACE, LEFT_FACE, TOP_FACE, BOTTOM_FACE = (
    0, 1, 2, 3, 4, 5)

# Directions. Enumerators increase in value turning in the clockwise direction.
# For each direction, adding 1 modulo 4 turns right, subtracting 1 modulo 4
# turns left, and adding 2 modulo 4 goes in the opposite direction.  The same
# enumerators can also name a panel edge, i.e., `EAST` names the eastern edge
# of a panel.
EAST, SOUTH, WEST, NORTH = 0, 1, 2, 3
DIR_NAMES = ('EAST', 'SOUTH', 'WEST', 'NORTH')

# Array of 2-tuples indexed by a direction, where each tuple corresponding to the
# (row-delta, column-delta) for moving in each of the four directions.
MOVE_DELTAS = ((0, 1), (1, 0), (0, -1), (-1, 0))

# The model cube is represented as a tuple of six faces, each of which has four
# adjacent faces.  Each entry in the array is indexed by a face and is
# represented as a tuple comprising the four adjacent faces in clockwise order,
# with an arbitrary starting point.
CUBE = ((RIGHT_FACE, BOTTOM_FACE, LEFT_FACE, TOP_FACE),  # FRONT_FACE
        (LEFT_FACE, BOTTOM_FACE, RIGHT_FACE, TOP_FACE),  # BACK_FACE
        (BACK_FACE, BOTTOM_FACE, FRONT_FACE, TOP_FACE),  # RIGHT_FACE
        (FRONT_FACE, BOTTOM_FACE, BACK_FACE, TOP_FACE),  # LEFT_FACE
        (FRONT_FACE, LEFT_FACE, BACK_FACE, RIGHT_FACE),  # TOP_FACE
        (BACK_FACE, LEFT_FACE, FRONT_FACE, RIGHT_FACE))  # BOTTOM_FACE

################# Classes #########################

class Panel:
    """Represent one panel of tiles, possibly mapped to a cube face"""

    def __init__(self, originRow, originCol, size, face, orientation):
        """Construct a panel representing the region of the board at the specified
        origin coordinates and extending `size` tiles to the right and down
        from the origin. The panel is mapped to the specified cube face,
        oriented with respect to adjacent faces as specified by `orientation`."""
        self.originRow   = originRow
        self.originCol   = originCol
        self.size        = size
        self.face        = face
        self.orientation = orientation

    def __repr__(self):
        """Return a string representation of this panel for debugging"""
        return f"Panel: origin = ({self.originRow}, {self.originCol}), " + \
               f"face = {self.face}, orientation = {self.orientation}"

    def isInbounds(self, row, col):
        """Return `True` if the coordinate `(row, col)` falls within this panel"""
        return (self.originRow <= row and row < self.originRow + self.size and
                self.originCol <= col and col < self.originCol + self.size)

    def exitEdgeOffset(self, row, col, direction):
        """Exiting this panel from `(row, col)`, in the specified `direction`,
        search counter-clockwise for the nearest corner and return the
        (clockwise) offset from that corner to the exit position."""

        # Get row and column relative to origin (i.e., make them zero based)
        relRow = row - self.originRow
        relCol = col - self.originCol

        # Get direction of offsets by rotating clockwise 90 degrees.
        # This computation is theoretically a matrix-multiplication problem,
        # but I've reduced it to a partial manual inner-product.
        rowMul, colMul = MOVE_DELTAS[(direction + 1) % 4]
        offset = relRow * rowMul + relCol * colMul
        if offset < 0: offset += self.size - 1
        return offset

    def entrancePosition(self, fromPanel, fromEdgeOffset):
        """Crossing a fold onto this this panel from `fromPanel` at
        `fromEdgeOffset`, compute and return the landing row, column, and new
        direction of movement on this panel."""

        bound = self.size - 1

        # Find from which direction we entered this panel
        for fromDirection in (EAST, SOUTH, WEST, NORTH):
            if self.orientation[fromDirection] == fromPanel.face:
                break

        # The new direction opposite the from direction
        direction = (fromDirection + 2) % 4

        # This computation can probably be done with a lookup rather than a
        # nested `if`, perhaps in combination with a matrix multiplication.
        # The edge offset calculation is not only the reverse of the one in
        # `exitEdgeOffset`, but is the mirror image, i.e., the offset is applied
        # in the counter-clockwise direction.
        if direction == EAST:
            relRow, relCol = fromEdgeOffset, 0
        elif direction == SOUTH:
            relRow, relCol = 0, bound - fromEdgeOffset
        elif direction == WEST:
            relRow, relCol = bound - fromEdgeOffset, bound
        elif direction == NORTH:
            relRow, relCol = bound, fromEdgeOffset

        row = self.originRow + relRow
        col = self.originCol + relCol
        return row, col, direction

################# Functions #########################

def calcCubeSide(board):
    """Return the length of each edge of a cube represented by `board`"""
    # Sum the number of non-space characters in all rows
    numTiles = 0
    for rowStr in board:
        numTiles += len(rowStr) - rowStr.count(' ')
    # Tiles are evenly distributed over 6 faces. Side length is square root of
    # number of tiles per face.
    return int(math.sqrt(numTiles // 6))

def foldAtEdge(board, fromPanel, fromPanelEdge):
    """Fold the board along the edge of `fromPanel` specified by `fromPanelEdge`;
    i.e., if `fromPanelEdge` is SOUTH then create a fold at the southern edge of
    `fromPanel`. Return the panel found on the other side of that edge or
    `None` if no panel is found in that direction."""
    size = fromPanel.size
    row, col = fromPanel.originRow, fromPanel.originCol
    drow, dcol = MOVE_DELTAS[fromPanelEdge]
    newRow = row + drow * size
    newCol = col + dcol * size
    if newRow < 0 or len(board)         <= newRow: return None
    if newCol < 0 or len(board[newRow]) <= newCol: return None
    if board[newRow][newCol] == ' ': return None

    newPanelEdge = (fromPanelEdge + 2) % 4  # WEST if fromPanelEdge is EAST, etc.

    face = fromPanel.orientation[fromPanelEdge]
    orientation = CUBE[face]  # Unoriented list of adjacencies

    # Rotate new panel's orientation until `newPanelEdge` is in the direction
    # of `fromPanel's` face.
    while orientation[newPanelEdge] != fromPanel.face:
        orientation = orientation[1:] + (orientation[0], )

    return Panel(newRow, newCol, fromPanel.size, face, orientation)

def foldCube(board, cubeSide):
    """Fold the flattened cube represented by `board`.  The first panel in the
    right-to-left, top-to-bottom order is mapped to the front face of the cube,
    and successive adjacent panels are wrapped around the cube. Return an array
    of cube faces."""

    cube = 6 * [ None ]

    # Create first panel in first row of panels and map it to FRONT_FACE.
    row = 0
    firstRow = board[row]
    col = min(firstRow.index('.'), firstRow.index('#'))
    panel = Panel(row, col, cubeSide, FRONT_FACE,
                  (RIGHT_FACE, BOTTOM_FACE, LEFT_FACE, TOP_FACE))
    cube[FRONT_FACE] = panel

    # Do a depth-first traversal of the panel list, mapping a face and
    # orientation to each panel.
    workqueue = [ panel ]
    while workqueue:
        panel = workqueue.pop()
        row, col = panel.originRow, panel.originCol
        for dir in (EAST, SOUTH, WEST, NORTH):
            if cube[panel.orientation[dir]]: continue  # Skip if already visited.
            nextPanel = foldAtEdge(board, panel, dir)
            if nextPanel:
                workqueue.append(nextPanel)
                cube[nextPanel.face] = nextPanel

    return cube

def move(board, cube, panel, row, col, direction, num):
    """Move `num` tiles in the specified `direction` and return the new panel,
    row, column, and direction"""
    size = panel.size
    for i in range(num):
        # Find next row.
        nextPanel = panel
        nextDir = direction
        drow, dcol = MOVE_DELTAS[direction]
        nextRow = row + drow
        nextCol = col + dcol
        # If reached edge of the panel, find landing position on next panel.
        if not panel.isInbounds(nextRow, nextCol):
            nextPanel                 = cube[panel.orientation[direction]]
            edgeOffset                = panel.exitEdgeOffset(row, col, direction)
            nextRow, nextCol, nextDir = nextPanel.entrancePosition(panel,
                                                                   edgeOffset)
        assert(nextPanel.isInbounds(nextRow, nextCol))
        if board[nextRow][nextCol] == '#':
            break  # Hit a wall; end loop without advancing
        else:
            # Advance to next tile
            panel, direction = nextPanel, nextDir
            row, col         = nextRow, nextCol

    assert(board[row][col] == '.')
    return panel, row, col, direction

################ main program #####################################3333

input = openInput.openInput(sys.argv)

board = [ line.rstrip() for line in input ]
path = board.pop()  # Last line of input
board.pop()         # Discard blank line at end

input.close()

cubeSize = calcCubeSide(board)
print(f"Cube is {cubeSize} on a side")

cube = foldCube(board, cubeSize)
print(cube)

# Find first column that is not '#' or space
panel = cube[FRONT_FACE]
direction = EAST
row = panel.originRow
col = board[row].index('.', panel.originCol)
assert(panel.isInbounds(row, col))

print(f"Start row, col = {row}, {col}")

# wo = panel.exitEdgeOffset(1, 0, WEST)
# print(f"exitEdgeOffset(1, 0, WEST) = {wo}")
# wr, wc, wd = cube[LEFT_FACE].entrancePosition(panel, wo)
# print(f"Land at ({wr}, {wc}) going {DIR_NAMES[wd]}")

# np, row, col, direction = move(board, cube, panel, 1, 0, WEST, 1)
# print(f"Land at ({row}, {col}) going {DIR_NAMES[direction]}")

numToMove = 0
# Appending '#' to path forces loop to execute a final time after the last digit
for c in path + '#':
    if c.isdigit():
        numToMove *= 10
        numToMove += int(c)
        continue

    panel, row, col, direction = move(board, cube, panel,
                                      row, col, direction, numToMove)
    numToMove = 0
    turn = 1 if c == 'R' else -1 if c == 'L' else 0
    direction = (direction + turn) % 4

# Change result from 0 indexed to 1 indexed
row += 1
col += 1
print(f"Landed at ({row}, {col}) heading {DIR_NAMES[direction]}")

password = row * 1000 + col * 4 + direction
print(f"password is {password}")
