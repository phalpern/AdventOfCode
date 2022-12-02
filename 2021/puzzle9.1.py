# Advent of Code day 9, part 1
# Risk of low points in cave floor

# 2-D array fo numbers 0 to 9
heightmap = [ ]

infile = open("puzzle9_input.txt", "r")

for line in infile:
    heightmap.append(list(map(int, line.rstrip())))

risk = 0
for i, row in enumerate(heightmap):
    for j, cell in enumerate(row):
        if i > 0 and heightmap[i - 1][j] <= cell:
            continue
        elif j > 0 and row[j - 1] <= cell:
            continue
        elif i < len(heightmap) - 1 and heightmap[i + 1][j] <= cell:
            continue
        elif j < len(row) - 1 and row[j + 1] <= cell:
            continue

        risk += cell + 1

        print("Lowpoint = ({}, {}), level = {}".format(i, j, cell))

print("Total risk = ", risk)
