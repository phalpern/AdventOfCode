# Advent of Code day 3, part 1
# Compute the gamma and epsilon rate from a diagnostic report

infile = open("puzzle3_input.txt", "r")   # Input: five bits per line

zeros = [ ]
ones  = [ ]

for str in infile:
    str = str.strip(" \n")
    while len(str) > len(zeros):
        zeros.append(0)
        ones.append(0)
    for pos in range(len(str)):
        if str[pos] == '0':
            zeros[pos] += 1
        else:
            ones[pos] += 1

gammaRate    = 0
epsilonRate  = 0

for pos in range(len(zeros)):
    gammaRate *= 2
    epsilonRate *= 2
    if ones[pos] > zeros[pos]:
        gammaRate += 1
    else:
        epsilonRate += 1

print("Gamma = {}, Epsilon = {}, product = {}".format(gammaRate, epsilonRate, \
                                                      gammaRate*epsilonRate))
