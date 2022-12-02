# Advent of Code day 9, part 2
# Three biggest basins

import copy

# 2-D array fo numbers 0 to 9
heightmap = [ ]

def basinSize(i, j):
    hm = copy.deepcopy(heightmap)   # Mutate `hm` as we traverse it
    workStack = [ (i, j) ]  # Cells to process

    def pushIfInBasin(cell, i, j):
        if i < 0 or i >= len(hm): return
        if i < 0 or j >= len(hm[i]): return
        newcell = hm[i][j]
        if newcell < 9 and newcell > cell:
            workStack.append((i, j))

    size = 0
    while workStack:
        i, j = workStack.pop()
        cell = hm[i][j]
        if cell >= 9: continue  # Don't visit an item twice
        size += 1
        pushIfInBasin(cell, i - 1, j)
        pushIfInBasin(cell, i, j - 1)
        pushIfInBasin(cell, i + 1, j)
        pushIfInBasin(cell, i, j + 1)
        hm[i][j] = 10  # Prevent backtracking to already-visted cells

    return size

infile = open("puzzle9_input.txt", "r")

for line in infile:
    heightmap.append(list(map(int, line.rstrip())))

largestBasins = [ 0, 0, 0 ]  # Three largest basins sizes
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

        basin = basinSize(i, j)
        print("Lowpoint = ({}, {}), basin = {}".format(i, j, basin))

        if basin > largestBasins[0]:
            largestBasins[0] = basin
            largestBasins.sort()

print("Largest basins = ", largestBasins, ", product = ",\
      largestBasins[0] * largestBasins[1] * largestBasins[2])
