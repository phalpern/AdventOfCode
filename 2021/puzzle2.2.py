# Advent of Code day 2, part 2
# Move the submarine according to the input instructions

infile = open("puzzle2_input.txt", "r")   # Input: One instruction per line

horizontal = 0  # Initial horizontal position
depth      = 0  # Initial depth
aim        = 0  # Vertical aim

for instruction in infile:
    [command, strval] = instruction.split()
    value = int(strval)
    if command == "forward":
        horizontal += value
        depth += value * aim
    elif command == "down":
        aim += value
    elif command == "up":
        aim -= value
    else:
        print("Invalid command: {}".format(command))

print("Position = {}, depth = {}, product = {}".format(horizontal, depth, \
                                                       horizontal*depth))
