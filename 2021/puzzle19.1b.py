# Advent of Code day 19, part 1
# How many beacons

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

                    # Filter beacons from `self` and `translatedOther` to
                    # include only those that are in the other one's bounding
                    # box.

                    otherBeacons = set(map(tuple,
                                           filter(lambda row :
                                                  self.inbounds(row),
                                                  translatedOther.beacons)))
                    if len(otherBeacons) < 12: continue

                    selfBeacons = set(map(tuple,
                                          filter(lambda row :
                                                 translatedOther.inbounds(row),
                                                 self.beacons)))
                    if len(selfBeacons) < 12: continue

                    # Only in the case of exact overlap of 12 or more items
                    # do we say that we have a match.
                    if otherBeacons == selfBeacons:
                        return translatedOther
        return None

infile = open("puzzle19_input.test.txt", "r")

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

allBeacons = set()
for scanner in matched:
    allBeacons.update(map(tuple, scanner.beacons))

print("Total beacons = ", len(allBeacons))
