# Advent of Code day 7, part 2
# Line up the crabs using a quadratic fuel-use formula

# Compute fuel use to move all crabs in `positions` to x. `positions` must be
# sorted in ascending order
def fuelUse(positions, x):
    ret = 0
    for pos in positions:
        if pos < x:
            delta = x - pos
        else:
            delta = pos - x
        ret += delta * (delta + 1) >> 1  # Sum of the numbers 1 to delta
    return ret

infile = open("puzzle7_input.txt", "r")

positions = [ ]
for str in infile.read().split(','):
    positions.append(int(str))

positions.sort()

# Compute fuel use for every position, choosing the smallest.
# Because the positions are sorted, if the fuel use goes up, then we've already
# seen the minimum.
#
# Note that there is probably a more efficient way to do this than to compute
# the fuel use for every position using trial and error, but I'm too tired
# today to figure out the algorithm.
bestSoFar = fuelUse(positions, 0)
for x in range(1, len(positions)):
    fuel = fuelUse(positions, x)
    if (fuel > bestSoFar):
        break
    else:
        bestSoFar = fuel

print("Optimal fuel use = ", bestSoFar)
