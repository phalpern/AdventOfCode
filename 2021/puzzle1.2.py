# Advent of Code, day 1, part 2.
# Print the number of times the moving sum of three consecutive items increases
# in the input sequence.

infile = open("puzzle1_input.txt", "r")   # Input sequence, one number per line

items = [ 0, 0, 0 ]                # Circular array of the 3 most recent items
items[0] = int(infile.readline())
items[1] = int(infile.readline())
items[2] = int(infile.readline())

increases = 0

windowA = items[0] + items[1] + items[2] # First window of 3 items
oldest = 0                               # Index of oldest item in `items` array

for line in infile:
    newitem = int(line)

    # New window's sum is computed by subtracting out the oldest item and
    # adding in the newest item.
    windowB = windowA - items[oldest] + newitem

    if windowB > windowA:
        increases += 1  # New window's sum is larger than previous window's sum

    windowA = windowB          # New window is now the old window
    items[oldest] = newitem    # Discard oldest item and replace by new item
    oldest = (oldest + 1) % 3  # Increment index to oldest item, circularly

print(increases)
