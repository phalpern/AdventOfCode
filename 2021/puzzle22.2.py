# Advent of Code day 22, part 2
# Reactor reboot with all steps

import copy

class Cuboid:
    
    def __init__(self, minCoord, maxCoord):
        self.minCoord = minCoord
        self.maxCoord = maxCoord

    def __repr__(self):
        return "({}, {})".format(self.minCoord, self.maxCoord)

    def copy(self):
        return copy.deepcopy(self)

    def volume(self):
        vol = 1
        for axis in range(3):
            vol *= self.maxCoord[axis] + 1 - self.minCoord[axis]
        return vol
        
    def intersects(self, other):
        """Returns True if this `Cuboid` interescts `other`"""
        for axis in range(3):
            if self.minCoord[axis] > other.maxCoord[axis] or self.maxCoord[axis] < other.minCoord[axis]:
                return False
        return True
    
    def intersection(self, other):
        """Return a single Cuboid that is the intersection of `self` and `other`"""
        minCoord = [0, 0, 0]
        maxCoord = [0, 0, 0]
        for axis in range(3):
            minCoord[axis] = max(self.minCoord[axis], other.minCoord[axis])
            maxCoord[axis] = min(self.maxCoord[axis], other.maxCoord[axis])
            if minCoord[axis] > maxCoord[axis]: return None  # No intersection
        return Cuboid(minCoord, maxCoord)

    def subtract(self, other):
        """Subtract other from self, yielding a list of one or more smaller Cuboids."""
        ret = []
        if not self.intersects(other) : return [ self ]
        current = self.copy()
        for axis in range(3):
            if other.minCoord[axis] > current.minCoord[axis]:
                newCuboid = current.copy()
                newCuboid.maxCoord[axis] = other.minCoord[axis] - 1
                ret.append(newCuboid)
                current.minCoord[axis] = other.minCoord[axis]
            if other.maxCoord[axis] < current.maxCoord[axis]:
                newCuboid = current.copy()
                newCuboid.minCoord[axis] = other.maxCoord[axis] + 1
                ret.append(newCuboid)
                current.maxCoord[axis] = other.maxCoord[axis]
        # After trimming away the non-intersecting parts, only the intersection remains
        i = self.intersection(other)
        assert(current.minCoord == i.minCoord)
        assert(current.maxCoord == i.maxCoord)
        vol = 0
        for r in ret:
            vol += r.volume()
        assert(vol == self.volume() - i.volume())
        return ret

    def fromString(str):
        coordStr = str.split(',')
        minCoord = [0] * 3
        maxCoord = [0] * 3
        for axis in range(3):
            mn, mx = coordStr[axis].split('..')            
            minCoord[axis] = int(mn[2:])
            maxCoord[axis] = int(mx)
        return Cuboid(minCoord, maxCoord)

def rebootStep(inputs, turnon, cuboid):
    outputs = []
    if turnon:
        outputs = inputs.copy()
        newCuboids = [ cuboid ]
        for ic in inputs:
            nextCuboidList = []
            for c in newCuboids:
                # To avoid counting any cubes twice, add only
                # the parts of `c` that don't intersect `ic`
                nextCuboidList.extend(c.subtract(ic))
            newCuboids = nextCuboidList
        outputs.extend(newCuboids)
    else:
        for ic in inputs:
            # Keep only the parts of `c` that don't intersect `cuboid`
            outputs.extend(ic.subtract(cuboid))
    return outputs

def rebootStepArray(cuboidMap, turnon, cuboid):
    for x in range(cuboid.minCoord[0] + 50, cuboid.maxCoord[0] + 51):
        for y in range(cuboid.minCoord[1] + 50, cuboid.maxCoord[1] + 51):
            for z in range(cuboid.minCoord[2] + 50, cuboid.maxCoord[2] + 51):
                cuboidMap[x, y, z] = turnon

def totalFromList(cuboids):
    total = 0
    for cuboid in cuboids:
        total += cuboid.volume()
    return total

infile = open("puzzle22_input.txt", "r")

cuboids = []
for stepline in infile:
    onoffStr, coords = stepline.rstrip().split(' ')
    cuboid = Cuboid.fromString(coords)
    cuboids = rebootStep(cuboids, onoffStr == 'on', cuboid)


total = totalFromList(cuboids)

# print(cuboids)
print("total on = ", total)
# print("array total = ", arrayTotal)