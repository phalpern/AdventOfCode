# Advent of Code day 6, part 2
# lanternfish population after 256 days

counterPopulations = [ 0, 0, 0, 0, 0, 0, 0, 0, 0 ]

infile = open("puzzle6_input.txt", "r")

for counterStr in infile.read().split(','):
    counter = int(counterStr)
    counterPopulations[counter] += 1

for day in range(256):
    spawn = counterPopulations[0]
    counterPopulations.pop(0)
    counterPopulations.append(spawn)
    counterPopulations[6] += spawn

population = 0
for counter in counterPopulations:
    population += counter

print("Population after 256 days = ", population)
