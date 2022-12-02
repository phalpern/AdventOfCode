# Advent of code day 25, part 1
# How many steps before the sea cucumbers top moving

import numpy as np

# Constants
class SeaMap:

    # Class constants
    Empty = 0
    East  = 1
    South = 2

    # Translation between symbols to `int` constants
    symbolToInt = { '.' : Empty, '>' : East, 'v' : South }
    intToSymbol = np.array([ '.', '>', 'v' ])

    def __init__(self):
        self.maparray = None

    def __str__(self):
        if self.maparray is None:
            return "None"
        else:
            result = ""
            asSymbols = self.intToSymbol[self.maparray]
            for row in asSymbols:
                result += ''.join(row) + '\n'
            return result

    def read(self, infile):
        maplist = []
        for line in infile:
            row = list(map(lambda x : self.symbolToInt[x], line.rstrip()))
            maplist.append(row)
        self.maparray = np.array(maplist)

    def moveEast(self):
        """Move east when possible. Return True on success False if no moves"""
        destMask = self.maparray == self.Empty
        srcMask  = self.maparray == self.East
        shiftedMask = np.concatenate((destMask[:,1:], destMask[:,0:1]), axis=1)
        srcMask  = srcMask & shiftedMask
        destMask = np.concatenate((srcMask[:,-1:], srcMask[:,0:-1]), axis=1)
        self.maparray[srcMask]  = self.Empty
        self.maparray[destMask] = self.East
        return srcMask.any()  # True if anything moved

    def moveSouth(self):
        """Move east when possible. Return True on success False if no moves"""
        destMask = self.maparray == self.Empty
        srcMask  = self.maparray == self.South
        shiftedMask = np.concatenate((destMask[1:,:], destMask[0:1,:]), axis=0)
        srcMask  = srcMask & shiftedMask
        destMask = np.concatenate((srcMask[-1:,:], srcMask[0:-1,:]), axis=0)
        self.maparray[srcMask]  = self.Empty
        self.maparray[destMask] = self.South
        return srcMask.any()  # True if anything moved

infile = open("puzzle25_input.txt", "r")

m = SeaMap()
m.read(infile)
steps = 0
while m.moveEast() | m.moveSouth():
    steps += 1

# print(f"After {steps} steps")
# print(m)
print(f"First failed step = {steps + 1}")
