# Advent of Code day 14, part 1
# Quantities of polymer elements

# Map an element pair to the element to insert between them.
pairInsertions  = { }

def readPairInsertions(infile):
    for line in infile:
        pair, inelem = line.rstrip().split(" -> ")
        pairInsertions[pair] = inelem

# Insert new element between the elements of each overlapping pair in `polymer`
# and return the result.
def insertElements(polymer):
    result = polymer[0]
    for i in range(0, len(polymer) - 1):
        pair = polymer[i:i+2]
        inelem = pairInsertions.get(pair, '')
        result += inelem + pair[1]
    return result

infile = open("puzzle14_input.txt", "r")

template = infile.readline().rstrip()
assert('\n' == infile.readline())  # Consume blank like
readPairInsertions(infile)

# Apply pair insertion 10 times
polymer = template
for i in range(10):
    polymer = insertElements(polymer)
    # print("After set {}: {} ".format(i + 1, polymer))

# Count min and max
elements = set(iter(polymer))
minCount = len(polymer)
maxCount = 0
for element in elements:
    count = polymer.count(element)
    print("count of '{}' = {}".format(element, count))
    if count < minCount: minCount = count
    if count > maxCount: maxCount = count

print("length = {}, min count = {}, max count = {}".format(len(polymer), minCount, maxCount))
print("maxCount - minCount = ", maxCount - minCount)
