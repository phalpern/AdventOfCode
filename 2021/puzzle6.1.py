# Advent of Code day 6, part 1
# lanternfish population after 80 days

counterPopulations = [ 0, 0, 0, 0, 0, 0, 0, 0, 0 ]

infile = open("puzzle6_input.txt", "r")

for counterStr in infile.read().split(','):
    counter = int(counterStr)
    counterPopulations[counter] += 1

for day in range(80):
    spawn = counterPopulations[0]
    counterPopulations.pop(0)
    counterPopulations.append(spawn)
    counterPopulations[6] += spawn

population = 0
for counter in counterPopulations:
    population += counter

print("Population after 80 days = ", population)
