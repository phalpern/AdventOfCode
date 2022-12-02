# Advent of Code day 8, part 2
# Some of all outputs

# Segment index to digit mapping:
#
#  aa
# b  c
#  dd
# e  f
#  gg

allsegs = { 'a', 'b', 'c', 'd', 'e', 'f', 'g' }

digitToSegs = [
    { 'a', 'b', 'c', 'e', 'f', 'g'       }, # 0
    { 'c', 'f'                           }, # 1
    { 'a', 'c', 'd', 'e', 'g'            }, # 2
    { 'a', 'c', 'd', 'f', 'g'            }, # 3
    { 'b', 'c', 'd', 'f'                 }, # 4
    { 'a', 'b', 'd', 'f', 'g'            }, # 5
    { 'a', 'b', 'd', 'e', 'f', 'g'       }, # 6
    { 'a', 'c', 'f'                      }, # 7
    { 'a', 'b', 'c', 'd', 'e', 'f', 'g'  }, # 8
    { 'a', 'b', 'c', 'd', 'f', 'g'       }  # 9
    ]

def segsToDigit(segs):
    for i, s in enumerate(digitToSegs):
        if s == segs:
            return i
    assert(0)

numsegsToSegUnion = {
    2 : digitToSegs[1],
    3 : digitToSegs[7],
    4 : digitToSegs[4],
    5 : digitToSegs[2].union(digitToSegs[3]).union(digitToSegs[5]),
    6 : digitToSegs[0].union(digitToSegs[6]).union(digitToSegs[9]),
    7 : digitToSegs[8]
    }

numsegsToSegIntersect = {
    2 : digitToSegs[1],
    3 : digitToSegs[7],
    4 : digitToSegs[4],
    5 : digitToSegs[2].intersection(digitToSegs[3]).intersection(digitToSegs[5]),
    6 : digitToSegs[0].intersection(digitToSegs[6]).intersection(digitToSegs[9]),
    7 : digitToSegs[8]
    }

infile = open("puzzle8_input.txt", "r")
inputLines = list(infile)

sum = 0
for line in inputLines:
    # Dictionary that maps unsolved remapped segments to possible solutions
    unsolved = {
        'a' : allsegs.copy(),
        'b' : allsegs.copy(),
        'c' : allsegs.copy(),
        'd' : allsegs.copy(),
        'e' : allsegs.copy(),
        'f' : allsegs.copy(),
        'g' : allsegs.copy()
        }

    # Dictionary that maps solves remapped segment to its correct value
    solved = { }

    patterns, outputs = [x.split() for x in line.split('|')]
    patterns.sort(key = lambda x : len(x))

    for pattern in patterns:
        for remappedSeg in pattern:
            unsolved[remappedSeg].intersection_update(numsegsToSegUnion[len(pattern)])

    while unsolved:
        for pattern in patterns:
            # print("pattern = ", pattern)
            notOneOf = numsegsToSegIntersect[len(pattern)].copy()
            notOneOf.update(solved.values())
            # print("notOneOf = ", notOneOf)
            for remappedSeg, partialSolution in unsolved.items():
                if pattern.find(remappedSeg) < 0:
                    partialSolution.difference_update(notOneOf)
                if len(partialSolution) == 1:
                    solved[remappedSeg] = next(iter(partialSolution))
                    unsolved.pop(remappedSeg)
                    break  # Modified dictionary; invalidate iteration

    resultVal = 0
    for output in outputs:
        resultVal *= 10
        resultVal += segsToDigit(set(map(lambda x : solved[x], output)))
    print("result = ", resultVal)
    sum += resultVal

print("sum = ", sum)
