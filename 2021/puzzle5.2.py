# Advent of Code day 5, part 2
# Count intersections of hydrothermal vents, including diagonals

import re

ventMap = { }  # Dictionary containing one entry per integer coordinate
               # containing at least one vent.

totalIntersections = 0

# Add entries to the map for the specified line.
# Keep track of intersections of at least two lines.
def markLine(x1, y1, x2, y2):
    global ventMap
    global totalIntersections

    xstep = 0
    if x1 < x2:
        xstep = 1
    elif x1 > x2:
        xstep = -1

    ystep = 0
    if y1 < y2:
        ystep = 1
    elif y1 > y2:
        ystep = -1

    x = x1
    y = y1
    while x != x2 + xstep or y != y2 + ystep:
        coordStr = str(x) + ',' + str(y)
        count = ventMap.get(coordStr, 0) + 1
        ventMap[coordStr] = count
        if count == 2:
            totalIntersections += 1
        x += xstep
        y += ystep

infile = open("puzzle5_input.txt", "r")

for lineStr in infile:
    [lineStartStr, lineEndStr] = re.split(" *-> *", lineStr)
    [x1Str, y1Str] = lineStartStr.split(',')
    [x2Str, y2Str] = lineEndStr.split(',')
    markLine(int(x1Str), int(y1Str), int(x2Str), int(y2Str))

print("Total intersections = {}".format(totalIntersections))
