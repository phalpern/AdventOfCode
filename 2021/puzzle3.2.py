# Advent of Code day 3, part 2
# Compute the oxygen generator and CO2 scrubber ratings from diagnostic input

infile = open("puzzle3_input.txt", "r")   # Input: five bits per line

# Examine the `pos` digit of each string in `data` and partition it into two
# arrays: where the specified digit is 1 and where the specified digit is 0. If
# `keepMost` is `True`, return the larger partition, otherwise return the
# smaller one.
def partitionPass(data, pos, keepMost):
    zeros = [ ]
    ones  = [ ]
    for str in data:
        if len(str) == 0:
            pass
        elif str[pos] == '0':
            zeros.append(str)
        else:
            ones.append(str)

    if keepMost:
        if len(zeros) > len(ones):
            return zeros
        else:
            return ones
    else:
        if len(zeros) > len(ones):
            return ones
        else:
            return zeros

# Repeatedly partition `data` based on each digit position until there is only
# one string left, which is then returned. At each step, keep the larger
# partition one if `keepMost` is `True` and the smaller one otherwise.
def findBest(data, keepMost):
    pos = 0
    while len(data) > 1:
        data = partitionPass(data, pos, keepMost)
        pos += 1
    return data[0]

# Convert a string of '0' and '1' digits into an integer
def bitstringToInt(str):
    result = 0
    for digit in str:
        result *= 2
        if digit == '1':
            result += 1
    return result

# Read the data file into an array of strings, one string per entry.
testdata = infile.read().split("\n")

oxygenGen   = bitstringToInt(findBest(testdata, True))
CO2Scrubber = bitstringToInt(findBest(testdata, False))

print("O2 = {}, CO2 = {}, life support = {}".format(oxygenGen, CO2Scrubber,
                                                    oxygenGen*CO2Scrubber))
