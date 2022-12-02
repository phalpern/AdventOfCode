# Advent of Code day 4, part 1
# Bingo

import re

# Represent the bingo board
class Board:
    squares  : [ ]                # 25 ints: 5x5 squares in row-major form
    rowMarks : [ 0, 0, 0, 0, 0 ]  # Count of marked squares on each row
    colMarks : [ 0, 0, 0, 0, 0 ]  # Count of marks on each row

    # Read a fresh board from an input file -- 5 lines with 5 numbers per line
    def read(self, infile):
        squarestrings = [ ]
        for row in range(5):
            squarestrings += re.split(' +', infile.readline().strip())
        assert len(squarestrings) == 25
        self.squares = [ ]
        self.rowMarks = [ 0, 0, 0, 0, 0 ]
        self.colMarks = [ 0, 0, 0, 0, 0 ]
        for str in squarestrings:
            self.squares.append(int(str))
        return self

    # Mark the specified number on the board.  Return True if bingo, else False.
    # If the number does not apear on the board, do nothing.
    # A marked square is represented by -1.
    def mark(self, num):
        if num in self.squares:
            index = self.squares.index(num)
            self.squares[index] = -1
            row = int(index / 5)
            col = index % 5
            self.rowMarks[row] += 1
            self.colMarks[col] += 1
            if self.rowMarks[row] == 5 or self.colMarks[col] == 5:
                return True  # Bingo!
        return False

    # Given the last number matched, return the score for this board
    def score(self, lastnum):
        accum = 0
        # Add up values of unmarked self.squares
        for sq in self.squares:
            if sq != -1:
                accum += sq
        return accum * lastnum

    def print(self):
        for row in range(5):
            rowstr = ""
            for col in range(5):
                index = row * 5 + col
                if self.squares[index] == -1:
                    rowstr += "  *"
                else:
                    rowstr += "{:>3}".format(self.squares[index])
            print(rowstr)
        print()

# Read a blank line. Return False if EOF, else True
def blankLine(infile):
    line = infile.readline()
    if not line: return False
    assert line == "\n"
    return True

# Read data file
infile = open("puzzle4_input.txt", "r")

randomSeq = [ ]
for ranStr in infile.readline().split(','):
    randomSeq.append(int(ranStr))

boards = [ ]
while blankLine(infile):
    boards.append(Board().read(infile))
infile.close()

for board in boards:
    board.print()

done = False
for ran in randomSeq:
    for board in boards:
        if board.mark(ran):
            print("Bingo on {}!".format(ran))
            board.print()
            print("Score = {}".format(board.score(ran)))
            done = True
            break
    if done:
        break
