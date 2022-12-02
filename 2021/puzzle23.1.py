# Advent of code day 23, part 1
# Minimum energy to organize amphipods

# String representing map is exactly 19 characters long. Each character
# is either '.' for an empty space or 'A', 'B', 'C', or 'D' for the specific
# amphipod type. The first 11 positions in the string represent the hallway.
# The remaining 8 positions represent the 4 desination rooms, two consecutive
# positions per rooom, with the first of the two representing the position
# closer to the hallway. The 'roomEncoding' dictionary maps each destination
# room to a tuple of its starting position within the string and the location
# of its entrance in the hallway:
mapEncoding = {
    'A' : (11, 2),
    'B' : (13, 4),
    'C' : (15, 6),
    'D' : (17, 8)
}

costPerMove = {
    'A' : 1,
    'B' : 10,
    'C' : 100,
    'D' : 1000
}

solution  = "...........AABBCCDD"
emptyHall = "..........."
excluded  = "..x.x.x.x.."   # x == spots you aren't allowed to land on.
firstRoom = mapEncoding['A'][0]

def moveAmphipod(mapStr, startCost, src, dest):
    """Move amphipod from `src` to `dest`, returning (newMap, newCost)"""
    distance = 0
    amphipod = mapStr[src]
    assert(amphipod != '.' and mapStr[dest] == '.')
    srcHall = src
    if src >= firstRoom:
        # `src` is in one of the rooms.  If odd, then front position, else in
        # back position:
        distance += 1 if (src & 1) == 1 else 2
        srcHall = ((src-1) | 1) - 9  # Compute room entrance from room pos
    destHall = dest
    if dest >= firstRoom:
        # `dest` is in one of the rooms.  If odd, then front position, else in
        # back position:
        distance += 1 if dest & 1 == 1 else 2
        destHall = ((dest-1) | 1) - 9 # Compute room entrance from room pos
    distance += abs(destHall - srcHall)
    # Swap src and dest
    if src < dest:
        newMap = "{}{}{}{}{}".format(mapStr[:src], mapStr[dest], mapStr[src+1:dest],
                                     mapStr[src], mapStr[dest+1:])
    else:
        newMap = "{}{}{}{}{}".format(mapStr[:dest], mapStr[src], mapStr[dest+1:src],
                                     mapStr[dest], mapStr[src+1:])
    return (newMap, startCost + distance * costPerMove[amphipod])

def nobrainers(mapStr, startCost):
    """Perform any "no-brainer" moves and return a tuple `(newMap, newCost)`
    A no-brainer is any move that will move an amphipod to its final
    position"""

    newCost = startCost
    changes = True
    while changes:
        changes = False

        # First, see if any amphipod in any room can move to its destination
        for room in ('A', 'B', 'C', 'D'):
            src, srcEntrance = mapEncoding[room]
            amphipod = mapStr[src]
            if amphipod == '.':
                src += 1
                amphipod = mapStr[src]
                if amphipod == '.': continue
            if amphipod == room: continue  # Same room move
            dest, destEntrance = mapEncoding[amphipod]
            roomMap = mapStr[dest:dest+2]
            if roomMap == '..':
                dest += 1
            elif roomMap != '.'+amphipod:
                continue
            i, j = (srcEntrance, destEntrance)
            if i > j:
                i, j = (j, i)  # Swap i and j so that i < j
            if (mapStr[i:j+1] != emptyHall[i:j+1]): continue  # Path not clear

            mapStr, newCost = moveAmphipod(mapStr, newCost, src, dest)
            changes = True
            break

        if changes: continue

        # If no changes above, check if any amphipod in the hallway can move to
        # its destination room.
        for src in range(len(emptyHall)):
            amphipod = mapStr[src]
            if amphipod == '.': continue
            dest, destEntrance = mapEncoding[amphipod]
            roomMap = mapStr[dest:dest+2]
            if roomMap == '..':
                dest += 1
            elif roomMap != '.'+amphipod:
                continue
            if src < destEntrance:
                i, j = (src + 1, destEntrance)
            else:
                i, j = (destEntrance, src - 1)
            if (mapStr[i+1:j+1] != emptyHall[i+1:j+1]): continue

            mapStr, newCost = moveAmphipod(mapStr, newCost, src, dest)
            changes = True
            break

    return (mapStr, newCost)

def addNextMove(mapStr, cost, src, dest, workQueue, memo):
    if excluded[dest] != '.': return
    mapStr, cost = moveAmphipod(mapStr, cost, src, dest)
    mapStr, cost = nobrainers(mapStr, cost)
    if mapStr in memo and memo[mapStr] <= cost: return
    memo[mapStr] = cost
    for i in range(len(workQueue)):
        if workQueue[i][0] == mapStr:
            workQueue[i] = (mapStr, cost)  # Replace in work queue
            return
    workQueue.append((mapStr, cost))

def processWorkQueue(workQueue, memo):
    mapStr, cost = workQueue.pop(0)  # Work on lowest cost map so far
    while mapStr != solution:
        for room in ('A', 'B', 'C', 'D'):
            src, srcHall = mapEncoding[room]
            roomMap = mapStr[src:src+2]
            if roomMap == '..' or roomMap == '.'+room or roomMap == room+room:
                # Room is empty or contains only amphipods that should already
                # be here.
                continue
            if mapStr[src] == '.':
                src += 1
            for dest in range(srcHall - 1, -1, -1):
                if mapStr[dest] != '.': break
                addNextMove(mapStr, cost, src, dest, workQueue, memo)
            for dest in range(srcHall + 1, len(emptyHall)):
                if mapStr[dest] != '.': break
                addNextMove(mapStr, cost, src, dest, workQueue, memo)
        workQueue.sort(key = lambda w : w[1])  # Sort by cost so far
        mapStr, cost = workQueue.pop(0)
    return cost

def solve(strMap):
    return processWorkQueue([ (strMap, 0) ], {} )

def readMap(infile):
    it = iter(infile)
    line = next(it)
    assert(line == "#############\n")
    line = next(it)
    assert(line == "#...........#\n")
    mapStr = emptyHall
    line1 = next(it)
    line2 = next(it)
    for room in ('A', 'B', 'C', 'D'):
        src, srcHall = mapEncoding[room]
        mapStr += line1[srcHall + 1] + line2[srcHall + 1]
    line = next(it)
    assert(line == "  #########\n")
    return mapStr

def printMap(mapStr):
    print("#############")
    print("#{}#".format(mapStr[:11]))
    print("###{}#{}#{}#{}###".format(mapStr[mapEncoding['A'][0]],
                                     mapStr[mapEncoding['B'][0]],
                                     mapStr[mapEncoding['C'][0]],
                                     mapStr[mapEncoding['D'][0]]))
    print("  #{}#{}#{}#{}#".format(mapStr[mapEncoding['A'][0] + 1],
                                   mapStr[mapEncoding['B'][0] + 1],
                                   mapStr[mapEncoding['C'][0] + 1],
                                   mapStr[mapEncoding['D'][0] + 1]))
    print("  #########")


infile = open("puzzle23_input.txt", "r")
mapStr = readMap(infile)
printMap(mapStr)
energy = solve(mapStr)
print("Min energy =", energy)

# mapStr, cost = nobrainers(mapStr, 4)
# print("Cost = ",cost)
# printMap(mapStr)
