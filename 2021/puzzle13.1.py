# Advent of Code day 13, part 1
# Fold up

# the dots up until the first blank line.  Return a set of (x, y) tuples.
def readDots(infile):
    dots = set()
    for line in infile:
        line = line.rstrip()
        if not line: break  # Stop at blank line
        dots.add(tuple(map(int, line.split(','))))
    return dots

# Fold at the specified axis and fold position.  Return updated set of dots
def fold(dots, axis, foldpos):
    newdots = set()

    # For each dot, compute new dot by reflecting dot in `foldpos`.
    # The formula for reflecting a coordinate is `foldpos + (foldpos - v)`,
    # where `v` is either the x coordinate or y coordinate.
    if axis == 'x':
        for dot in dots:
            if dot[0] > foldpos:
                newdot = ( foldpos + foldpos - dot[0], dot[1] )
            else:
                newdot = dot
            newdots.add(newdot)
    else:
        for dot in dots:
            if dot[1] > foldpos:
                newdot = ( dot[0], foldpos + foldpos - dot[1] )
            else:
                newdot = dot
            newdots.add(newdot)

    return newdots

# Parse one fold instruction from the input file.  Return a tuple ('x', #) or
# ('y', #), where 'x' or 'y' is the axis and # is the value.  A return value of
# `('x', 2)` would be a vertical line at x = 2, whereas `('y', 9)` would be a
# horizontal line at y = 9.
def parseFold(line):
    line = line.rstrip()
    assert(line.startswith("fold along "))
    axis, val = line[len("fold along "):].split('=')
    assert(axis == 'x' or axis == 'y')
    return ( axis, int(val) )

infile = open("puzzle13_input.txt", "r")

# Set of dots on the sheet
dots = readDots(infile)

# Execute only the first fold
line = infile.readline()
axis, foldpos = parseFold(line)
dots = fold(dots, axis, foldpos)

print("Unique dots = ", len(dots))
