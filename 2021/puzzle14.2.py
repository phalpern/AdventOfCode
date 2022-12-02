# Advent of Code day 14, part 2
# Quantities of polymer elements after 40 steps

# Given an insertion rule `AB -> C`, map the initial pair to two pairs:
# `AB -> [ AC, CB ]`
pairSplits = { }

def readPairSplits(infile):
    for line in infile:
        pair, inelem = line.rstrip().split(" -> ")
        pairSplits[pair] = [ pair[0] + inelem, inelem + pair[1] ]

# Increment `dict[key]` by `incr`.  If `dict[key]` doesn't already exist, set
# it to `0` before incrementing it.
def incrementKey(dict, key, incr=1):
    dict[key] = dict.get(key, 0) + incr

# Logically insert a new element between the elements of each overlapping pair
# in `pairFrequencies`, which maps each letter pair to the frequency it occurs
# in the polymer. Return the result.
def insertElements(pairFrequencies):
    result = { }
    for pair, freq in pairFrequencies.items():
        split1, split2 = pairSplits[pair]
        incrementKey(result, split1, freq)
        incrementKey(result, split2, freq)
    return result

# Return a map of single letters to frequencies. The `pairFrequencies` map is
# assumed to count every letter twice (as part of two pairs) but the first and
# last letter in the `template` string are each counted one fewer time.
def countFrequencies(pairFrequencies, template):
    result = { }
    for pair, freq in pairFrequencies.items():
        incrementKey(result, pair[0], freq)
        incrementKey(result, pair[1], freq)
    incrementKey(result, template[0])
    incrementKey(result, template[-1])
    for letter in result:
        result[letter] >>= 1
    return result

infile = open("puzzle14_input.txt", "r")

template = infile.readline().rstrip()
assert('\n' == infile.readline())  # Consume blank like
readPairSplits(infile)

pairFrequencies = { }
for i in range(len(template) - 1):
    pair = template[i : i + 2]
    incrementKey(pairFrequencies, pair)
# print("initial pair frequencies = ", pairFrequencies)

# Apply pair insertion 40 times
for i in range(40):
    pairFrequencies = insertElements(pairFrequencies)
    # print("After set {}: {} ".format(i + 1, pairFrequencies))

# Count min and max
minCount = 0
maxCount = 0
for element, count in countFrequencies(pairFrequencies, template).items():
    print("count of '{}' = {}".format(element, count))
    if minCount == 0 or count < minCount: minCount = count
    if count > maxCount: maxCount = count

print("min count = {}, max count = {}".format(minCount, maxCount))
print("maxCount - minCount = ", maxCount - minCount)
