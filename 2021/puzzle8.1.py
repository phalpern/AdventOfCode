# Advent of Code day 8, part 1
# How many times for digits 1, 4, 7, or 8 in scrambled display

numSegsToDigit = {
    2 : 1,
    4 : 4,
    3 : 7,
    7 : 8
    }

infile = open("puzzle8_input.txt", "r")

result = 0
for line in infile:
    # patternStr, outputStr = line.split('|')
    # patterns = patternStr.split()
    # outputs = outputStr.split()
    patterns, outputs = [x.split() for x in line.split('|')]
    # patterns, outputs = list(map(lambda x : x.split(), line.split('|')))
    for segments in outputs:
        if numSegsToDigit.get(len(segments), False):
            result += 1

print("Count of 1, 4, 7, or 8 = ", result)
