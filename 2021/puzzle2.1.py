# Advent of Code day 2, part 1
# Move the submarine according to the input instructions

infile = open("puzzle2_input.txt", "r")   # Input: One instruction per line

horizontal = 0  # Initial horizontal position
depth      = 0  # Initial depth

for instruction in infile:
    [command, strval] = instruction.split()
    value = int(strval)
    if command == "forward":
        horizontal += value
    elif command == "down":
        depth += value
    elif command == "up":
        depth -= value
    else:
        print("Invalid command: {}".format(command))

print("Position = {}, depth = {}, product = {}".format(horizontal, depth, \
                                                       horizontal*depth))
