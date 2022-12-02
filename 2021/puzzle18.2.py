# Advent of code day 18, part 1
# Sum of pairs of snailfish numbers

# A snailfish number is represented as a list of two elements, each of which
# might be a regular number (`int`) or a nested list.

def addToLeftmost(node, addval):
    """Add `addval` to the leftmost leaf of the specified `node`"""
    if addval == None:
        return node
    elif type(node) == int:
        return node + addval
    else:
        left, right = node
        return (addToLeftmost(left, addval), right)

def addToRightmost(node, addval):
    """Add `addval` to the rightmost leaf of the specified `node`"""
    if addval == None:
        return node
    elif type(node) == int:
        return node + addval
    else:
        left, right = node
        return (left, addToRightmost(right, addval))

def reduceExplode(node, depth):
    """Return (changed, newnode, addLeft, addRight)"""
    if type(node) == int:
        # Leaf node
        return (False, node, None, None)

    left, right = node  # Unpack tuple
    if depth >= 4 and type(left) == int and type(right) == int:
        # Explode node and replace with 0
        # print("Explode", node)
        return (True, 0, left, right)

    changed, newNode, addLeft, addRight = reduceExplode(left, depth + 1)
    if changed:
        # left node (or subnode) exploded
        left = newNode
        right = addToLeftmost(right, addRight)
        return (changed, (left, right), addLeft, None)

    changed, newNode, addLeft, addRight = reduceExplode(right, depth + 1)
    if changed:
        # right node (or subnode) exploded
        left = addToRightmost(left, addLeft)
        right = newNode
        return (changed, (left, right), None, addRight)

    # No change
    return (False, node, None, None)

def reduceSplit(node):
    """Return (changed, newnode)"""
    if type(node) == int:
        if node >= 10:
            # Split: Replace node with (node / 2, node / 2)
            # print("Split",node)
            left = node >> 1
            right = node - left
            return (True, (left, right))
        else:
            # No change
            return (False, node)

    left, right = node

    changed, left = reduceSplit(left)
    if not changed:
        changed, right = reduceSplit(right)

    # if chnaged, one of the nodes (or subnodes) split and was replaced
    return (changed, (left, right))

def reduce(sfNum):
    """Reduce the snailfish number and return the result."""
    changed = True
    while changed:
        # print("step:",sfNum)
        changed, sfNum, l, r = reduceExplode(sfNum, 0)
        if changed:
            continue
        changed, sfNum = reduceSplit(sfNum)

    return sfNum

def add(n1, n2):
    """Add two snailfish numbers and return the results"""
    return reduce((n1, n2))

def magnitude(sfNum):
    if type(sfNum) == int:
        return sfNum
    else:
        left, right = sfNum
        return 3 * magnitude(left) + 2 * magnitude(right)

def parsePair(c, strIter):
    """Parse the pair in the sequence `c, next(strIter)...`."""
    """Return (nextchar, pair)"""
    assert(c == '[')
    c = next(strIter)
    (c, left) = parsePair(c, strIter) if c == '[' else parseNumber(c, strIter)
    assert(c == ',')
    c = next(strIter)
    (c, right) = parsePair(c, strIter) if c == '[' else parseNumber(c, strIter)
    assert(c == ']')
    c = next(strIter)
    return (c, (left, right))

def parseNumber(c, strIter):
    """Parse the regular number in the sequence `c, next(strIter)...`."""
    """Return (nextchar, number)"""
    numstr = ''
    while c.isdigit():
        numstr = numstr + c
        c = next(strIter)
    assert(numstr)
    return (c, int(numstr))

def parseSnailfishNumber(string):
    """Parse and return the snailfish number in `string` Note that `string`"""
    """must be a syntactically valid snailfish number followed by a newline."""
    # Parse by recursive descent
    assert(string[-1] == '\n')
    strIter = iter(string)
    c = next(strIter)
    (c, ret) = parsePair(c, strIter)
    assert(c == '\n')
    return ret

# print(reduce((((((9,8),1),2),3),4)))
# print(reduce(((6,(5,(4,(3,2)))),1)))
# print(reduce(((3,(2,(1,(7,3)))),(6,(5,(4,(3,2)))))))
# print(reduce((((((4,3),4),4),(7,((8,4),9))),(1,1))))

infile = open("puzzle18_input.txt", "r")

def printMax(sfnumbers):
    max = 0
    for i in range(len(sfnumbers)):
        for j in range(i+1, len(sfnumbers)):
            mag = magnitude(add(sfnumbers[i], sfnumbers[j]))
            if mag > max: max = mag
            mag = magnitude(add(sfnumbers[j], sfnumbers[i]))
            if mag > max: max = mag
    print("max pairwise magnitude =", max)

sfnumbers = [ ]
for line in infile:
    if line == '\n':
        printMax(sfnumbers)
        sfnumbers = [ ]
        continue
    sfnumbers.append(parseSnailfishNumber(line))

printMax(sfnumbers)
