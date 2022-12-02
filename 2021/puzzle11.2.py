# Advent of Code day 11, part 2
# First step of synchronization

grid = []

# Increment every value in the grid
def incrementValues():
    global grid
    for row in grid:
        for j in range(len(row)):
            row[j] += 1

# Increment every value surrounding `grid[i][j]`.  Do not increment values of
# zero (which have already flashed this turn).
def incrementSurrounding(i, j):
    global grid
    for x, y in [
            (i-1, j-1), (i-1, j  ), (i-1, j+1),
            (i  , j-1),             (i  , j+1),
            (i+1, j-1), (i+1, j  ), (i+1, j+1)
            ]:
        if 0 <= x and x < len(grid)    and \
           0 <= y and y < len(grid[x]) and grid[x][y] != 0:
            grid[x][y] += 1

# Flash cell at `(i, j)` and return number of cells flashed (i.e., 1)
def flash(i, j):
    grid[i][j] = 0
    incrementSurrounding(i, j)
    return 1

infile = open("puzzle11_input.txt", "r")

for line in infile:
    grid.append(list(map(int, line.rstrip())))

gridSize = len(grid) * len(grid[0])

for step in range(1000000):  # Limit to 1M to avoid possible endless loop
    stepFlashes = 0

    # Phase a: Increment all of the values
    incrementValues()

    # Phases b and c: Flash any values > 9 and set values to 0
    # Repeat so long as new flashes were detected
    newFlashes = True
    while newFlashes:
        newFlashes = False
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j] > 9:
                    stepFlashes += flash(i, j)
                    newFlashes = True

    if stepFlashes == gridSize:
        print("Synchronized at step ", step + 1)
        break
