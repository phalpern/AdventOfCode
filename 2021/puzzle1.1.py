# Advent of Code day 1, part 1
# Print the number of times the value of the input sequence increases over the
# previous value.

infile = open("puzzle1_input.txt", "r"); # Input sequence, one number per line
sum = 0
prev = int(infile.readline()) # First value

for line in infile:
    curr = int(line)
    if curr > prev:
        sum += 1
    prev = curr

print(sum)
