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
import re

input = openInput.openInput(sys.argv)

dir=0
file=1

class DirNode:
    """Class representing a directory node"""
    def __init__(self, name):
        self.name = name
        self.size = None
        self.entries = dict()

    def __str__(self):
        return f"{self.name} (dir, size={self.calcSize()})"

    def addEntry(self, entry):
        self.entries[entry.name] = entry

    def getEntry(self, entryname):
        return self.entries[entryname]

    def calcSize(self):
        if not (self.size is None): return self.size
        size = 0
        for entry in self.entries.values():
            size += entry.calcSize()
        self.size = size
        return size

    def format(self, indent = ""):
        """Recursively print directory with specified indent"""
        print(f"{indent}- {str(self)}")
        for entry in self.entries.values():
            entry.format(indent + "  ")

class FileNode:
    """Class representing a file node"""
    def __init__(self, name, size):
        self.name = name
        self.size = size

    def __str__(self):
        return f"{self.name} (file, size={self.calcSize()})"

    def calcSize(self):
        return self.size

    def format(self, indent = ""):
        """print file and size with specified indent"""
        print(f"{indent}- {str(self)}")

class FlatDirIter:
    """Iterator to traverse a directory and its subdirectory as a flat set of
    entries"""
    def __init__(self, rootentry):
        # Current iterator iterates over a one-element list containing the root entry
        self.curriter = iter([ rootentry ])
        self.iterstack = [ ]

    def __iter__(self):
        return self

    def __next__(self):
        """Return the next entry in the sequence or else throw"""
        while not (self.curriter is None):
            try:
                nextitem = next(self.curriter)
                if type(nextitem) is DirNode:
                    self.iterstack.append(self.curriter)
                    self.curriter = iter(nextitem.entries.values())
                return nextitem
            except:
                self.curriter = self.iterstack.pop() if self.iterstack else None
        raise StopIteration

root = DirNode("/")
path = [root]  # path to current working directory
cwd  = root    # current working directory

ls = False
for line in input:
    line = line.rstrip()
    if line == "$ cd /":
        path = [root]
        cwd  = root
        ls = False
    elif line == "$ cd ..":
        path.pop()
        cwd = path[-1]
        ls = False
    elif line.startswith("$ cd "):
        path.append(cwd.getEntry(line[5:].lstrip()))
        cwd = path[-1]
        ls = False
    elif line == "$ ls":
        ls = True
    elif line.startswith("dir "):
        assert(ls)
        cwd.addEntry(DirNode(line[4:].lstrip()))
    else:
        assert(ls)
        match = re.match(r'^([0-9]*) *(.*)$', line)
        assert(match)
        cwd.addEntry(FileNode(match[2], int(match[1])))

# root.format()

limit=100000
totalWithinLimit = 0

print(f"Directories no larger than {limit}")
for entry in FlatDirIter(root):
    if type(entry) is DirNode:
        if entry.calcSize() <= limit:
            totalWithinLimit += entry.calcSize()
            print(entry)

print(f"Total = {totalWithinLimit}")
