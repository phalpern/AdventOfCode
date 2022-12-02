# Advent of code day 17, part 2
# How many velocities

import math

def computePos(xi, yi, steps):
    """Given initial velocity `(xi, yi)` return position of probe, `(x, y)`
    after the specified number of `steps`"""

    # If not constrained, given initial velocity i and change in velocity of -1
    # per step, the position after the specified number of `steps` is
    # `steps * i - (steps - 1) * steps / 2`

    # Compute x position as though `xi` were positive, and clamp x velocity at
    # zero.  Apply sign after computation:
    xsign = -1 if xi < 0 else 1
    xi_abs = xi * xsign
    xsteps = steps if steps <= xi_abs else xi_abs  # Clamp to zero velocity
    x = xsign * (xsteps * xi_abs - (((xsteps - 1) * xsteps) >> 1))

    y = steps * yi - (((steps - 1) * steps) >> 1)

    return (x, y)

def testComputePos(xi, yi):

    print("Testing starting velocity {}".format((xi, yi)))

    x = 0
    y = 0
    vx = xi
    vy = yi

    for steps in range(10):
        check = computePos(xi, yi, steps)
        if check[0] != x or check[1] != y:
            print("After {} steps, expected {}, got {}".format(steps, (x, y), check))
        x += vx
        if vx < 0:
            vx += 1
        elif vx > 0:
            vx -= 1

        y += vy
        vy -= 1

# for xi in range(-5, 6):
#     for yi in range(-5, 6):
#         testComputePos(xi, yi)



# Target is a tuple (xmin, xmax, ymin, ymax)
test_target = (20, 30, -10, -5)
real_target = (253, 280, -73, -46)

target = real_target

# Assume that for any positive y velocity yi, the probe will reach a
# velocity of -yi just as it reaches the starting height, then go down another
# yi + 1 below zero.  Therefore, the maximum for yi should be -ymin-1,
# reaching apogy after step -ymin-1, and hitting the target after step
# -2*ymin + 2. Test around those limits:

(targXmin, targXmax, targYmin, targYmax) = target
solutions = set()
minYi = -targYmax
minXi = int(math.sqrt(targXmin * 2 + 2))
maxXi = targXmax
for yi in range(targYmin, 1):
    for steps in range(1, -targYmin):
        (checkX, checkY) = computePos(0, yi, steps)
        if checkY > targYmax:
            continue
        elif checkY < targYmin:
            break
        else:
            # Found a working `yi` and `steps`, now find working `xi` values
            for xi in range(minXi, maxXi + 1):
                (checkX, checkY) = computePos(xi, yi, steps)
                if checkX < targXmin:
                    continue
                elif checkX > targXmax:
                    break
                else:
                    solutions.add((xi, yi))

            # For each working `yi`, `-yi-1` will also work, increasing
            # `steps` by `-2*yi-1` as well.
            yi2 = -yi-1
            steps2 = steps + 2*yi2 + 1
            for xi in range(minXi, maxXi + 1):
                (checkX, checkY) = computePos(xi, yi2, steps2)
                if checkX < targXmin:
                    continue
                elif checkX > targXmax:
                    break
                else:
                    solutions.add((xi, yi2))

# print("solutions =", solutions)
print("num solutions =", len(solutions))
