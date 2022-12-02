# Advent of Code day 19, part 2
# Largest Manhattan distance

import numpy as np
import copy

mat = np.array

# There are 24 possible rotations.  For each rotation there is a 3x3 matrix
# Multiplying a list of points by one of these matrices yields a rotated list
# of points.
rotations = (
    mat([ ( 1,  0,  0), ( 0,  1,  0),  ( 0,  0,  1) ]),
    mat([ ( 1,  0,  0), ( 0,  0,  1),  ( 0, -1,  0) ]),
    mat([ ( 1,  0,  0), ( 0, -1,  0),  ( 0,  0, -1) ]),
    mat([ ( 1,  0,  0), ( 0,  0, -1),  ( 0,  1,  0) ]),

    mat([ ( 0,  1,  0), (-1,  0,  0),  ( 0,  0,  1) ]),
    mat([ ( 0,  1,  0), ( 0,  0, -1),  (-1,  0,  0) ]),
    mat([ ( 0,  1,  0), ( 1,  0,  0),  ( 0,  0, -1) ]),
    mat([ ( 0,  1,  0), ( 0,  0,  1),  ( 1,  0,  0) ]),

    mat([ ( 0,  0,  1), ( 0,  1,  0),  (-1,  0,  0) ]),
    mat([ ( 0,  0,  1), ( 1,  0,  0),  ( 0,  1,  0) ]),
    mat([ ( 0,  0,  1), ( 0, -1,  0),  ( 1,  0,  0) ]),
    mat([ ( 0,  0,  1), (-1,  0,  0),  ( 0, -1,  0) ]),

    mat([ (-1,  0,  0), ( 0, -1,  0),  ( 0,  0,  1) ]),
    mat([ (-1,  0,  0), ( 0,  0, -1),  ( 0, -1,  0) ]),
    mat([ (-1,  0,  0), ( 0,  1,  0),  ( 0,  0, -1) ]),
    mat([ (-1,  0,  0), ( 0,  0,  1),  ( 0,  1,  0) ]),

    mat([ ( 0, -1,  0), ( 1,  0,  0),  ( 0,  0,  1) ]),
    mat([ ( 0, -1,  0), ( 0,  0,  1),  (-1,  0,  0) ]),
    mat([ ( 0, -1,  0), (-1,  0,  0),  ( 0,  0, -1) ]),
    mat([ ( 0, -1,  0), ( 0,  0, -1),  ( 1,  0,  0) ]),

    mat([ ( 0,  0, -1), ( 0,  1,  0),  ( 1,  0,  0) ]),
    mat([ ( 0,  0, -1), ( 1,  0,  0),  ( 0, -1,  0) ]),
    mat([ ( 0,  0, -1), ( 0, -1,  0),  (-1,  0,  0) ]),
    mat([ ( 0,  0, -1), (-1,  0,  0),  ( 0,  1,  0) ])
    )

class Scanner:

    def __init__(self, beacons):
        self.beacons = np.array(beacons)
        self.center = np.array((0, 0, 0))
        self.boundaryMin = np.array((-1000, -1000, -1000))
        self.boundaryMax = np.array(( 1000,  1000,  1000))
        self.rotationMemo = [ None ] * len(rotations)
        self.rotationMemo[0] = self.beacons

    def __str__(self):
        return str(self.beacons)

    def read(infile):
        """Reads beacons as coordinates up to and including empty line (or eof)"""
        beacons = []
        for line in infile:
            if line == '\n': break
            beacons.append(tuple(map(int, line.rstrip().split(','))))
        return Scanner(beacons)

    def rotate(self, rotationMatrix):
        """Rotate scanner. Return a new scanner."""
        return Scanner(np.matmul(self.beacons, rotationMatrix))

    def translate(self, translationVector):
        """Translate scanner. Return a new scanner."""
        ret = Scanner(np.apply_along_axis(lambda x : x + translationVector,
                                          axis=1, arr=self.beacons))
        ret.center      += translationVector
        ret.boundaryMin += translationVector
        ret.boundaryMax += translationVector
        return ret

    def inbounds(self, beacon):
        """Return True if beacon is within the boundary box for this scanner"""
        return ((self.boundaryMin <= beacon).all() and
                (self.boundaryMax >= beacon).all())

    def overlapsWith(self, other):
        """Returns the correctly rotated and translated version of `other` if it
        overlaps with `self` by at least 12 beacons, else `None`."""
        selfBeacons = set(map(tuple, self.beacons))
        for rotation in rotations:
            rotatedOther = other.rotate(rotation)
            translations = set()
            for selfPoint in self.beacons:
                for otherPoint in rotatedOther.beacons:
                    translation = tuple(selfPoint - otherPoint)
                    if translation in translations:
                        continue
                    translations.add(translation)
                    translatedOther = rotatedOther.translate(translation)
                    otherBeacons = set(map(tuple, translatedOther.beacons))
                    commonBeacons = selfBeacons.intersection(otherBeacons)
                    if len(commonBeacons) < 12:
                        continue

                    # return translatedOther

                    # Any `translatedOther` beacons outside of intersection
                    # must also be outside the boundaries of `self`, otherwise,
                    # overlap test fails.
                    inBounds = False
                    for beacon in otherBeacons.difference(commonBeacons):
                        if self.inbounds(beacon):
                            inBounds = True
                            break
                    if inBounds : continue

                    # Any `self` beacons outside of intersection must also be
                    # outside the boundaries of `translatedOther`, otherwise,
                    # overlap test fails.
                    for beacon in selfBeacons.difference(commonBeacons):
                        if translatedOther.inbounds(beacon):
                            inBounds = True
                            break
                    if inBounds : continue

                    # If got here, then we have a match!
                    return translatedOther
        return None

infile = open("puzzle19_input.txt", "r")

scanners = []
for line in infile:
    # `line` is "--- scanner # ---\n"
    # print('\n', line)
    scanners.append(Scanner.read(infile))
infile.close()
print("Read {} scanners".format(len(scanners)))

numScanners = len(scanners)
matched = [ scanners.pop(0) ]
unmatched = scanners

# Can't use a `for` loop because `len(matched)` changes during iteration
matchedIndex = 0
while matchedIndex < len(matched):
    known = matched[matchedIndex]
    unmatchedIndex = 0
    while unmatchedIndex < len(unmatched):
        overlapper = known.overlapsWith(unmatched[unmatchedIndex])
        if overlapper:
            matched.append(overlapper)
            unmatched.pop(unmatchedIndex)
            print("Found match {} of {}".format(len(matched), numScanners))
        else:
            unmatchedIndex += 1
    matchedIndex += 1

assert(len(unmatched) == 0)

largestDistance = 0
scannerCoords = list(map(lambda s : s.center, matched))
for i in range(len(scannerCoords)):
    for j in range(i+1, len(scannerCoords)):
        xyzDistance = tuple(map(abs, scannerCoords[i] - scannerCoords[j]))
        manhattanDistance = np.sum(xyzDistance)
        if manhattanDistance > largestDistance:
            largestDistance = manhattanDistance

print("Largest distance =", largestDistance)
