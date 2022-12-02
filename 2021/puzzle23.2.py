# Advent of code day 23, part 2
# Minimum energy to organize 16 amphipods (instead of 8)

from nis import maps
import re

# String representing map is exactly 27 characters long. Each character
# is either '.' for an empty space or 'A', 'B', 'C', or 'D' for the specific
# amphipod type. The first 11 positions in the string represent the hallway.
# The remaining 16 positions represent the 4 desination rooms, four consecutive
# positions per rooom, with the first of the four representing the position
# closest to the hallway. The 'roomEncoding' dictionary maps each destination
# room to a tuple of its starting position within the string and the location
# of its entrance in the hallway:
mapEncoding = {
    'A' : (11, 2),
    'B' : (15, 4),
    'C' : (19, 6),
    'D' : (23, 8)
}

costPerMove = {
    'A' : 1,
    'B' : 10,
    'C' : 100,
    'D' : 1000
}



solution  = "...........AAAABBBBCCCCDDDD"
emptyHall = "..........."
excluded  = "..x.x.x.x.."   # x == spots you aren't allowed to land on.
firstRoom = mapEncoding['A'][0]

def strSwapChars(s, pos1, pos2):
    """Swap the character in `s` at `pos1` with the character at `pos2` and
    return the resulting string"""
    if pos1 > pos2:
        # Swap `pos1` and `pos2` so that `pos1` is smaller
        pos2, pos1 = (pos1, pos2)
    return s[:pos1] + s[pos2] + s[pos1+1:pos2] + s[pos1] + s[pos2+1:]

def moveAmphipod(mapStr, startCost, src, dest):
    """Move amphipod from `src` to `dest`, returning (newMap, newCost)"""
    distance = 0
    amphipod = mapStr[src]
    assert(amphipod != '.' and mapStr[dest] == '.')
    srcHall = src
    if src >= firstRoom:
        # `src` is in one of the rooms.
        distance += 1 + (src - firstRoom) % 4
        # Compute room entrance from room pos
        srcHall = 2 + 2 * ((src - firstRoom) // 4)
    destHall = dest
    if dest >= firstRoom:
        # `dest` is in one of the rooms.
        distance += 1 + (dest - firstRoom) % 4
        # Compute room entrance from room pos
        destHall = 2 + 2 * ((dest - firstRoom) // 4)
    distance += abs(destHall - srcHall)
    newMap = strSwapChars(mapStr, src, dest)
    return (newMap, startCost + distance * costPerMove[amphipod])

def roomInsertPoint(mapStr, roomId):
    """Return the position and hall entrance in `mapStr` where an amphipod
    matching `roomId` can be inserted into the room specified by `roomId`, or
    else return `None`."""
    pos, entrance = mapEncoding[roomId]
    pat = re.compile(r'(\.{1,4})%s{0,3}' % roomId)
    m = pat.fullmatch(mapStr, pos, pos + 4)
    if m:
        return (m.end(1) - 1, entrance)
    return (None, None)

def roomRemovePoint(mapStr, roomId):
    """Return the postion and hall entrance in `mapStr` where an amphipod can
    be removed from the room specified by `roomId`, or else return `None`."""
    pos, entrance = mapEncoding[roomId]
    if re.compile(r'\.*%s*' % roomId).fullmatch(mapStr, pos, pos + 4):
        return (None, None)  # Don't move anything from its final position
    pat = re.compile(r'\.{0,3}([A-D]{1,4})')
    m = pat.fullmatch(mapStr, pos, pos + 4)
    if m:
        return (m.start(1), entrance)
    return (None, None)

def nobrainers(mapStr, startCost):
    """Perform any "no-brainer" moves and return a tuple `(newMap, newCost)`
    A no-brainer is any move that will move an amphipod to its final
    position"""

    newCost = startCost
    changes = True
    while changes:
        changes = False

        for amphipod in ('A', 'B', 'C', 'D'):
            # First, see if any amphipod in any room can accept a new amphipod
            dest, destEntrance = roomInsertPoint(mapStr, amphipod)
            if not dest: continue

            # Next, create a list of possible sources for the amphipod
            sources = []

            # List any rooms that can provide the destination amphipod
            for srcRoomId in ('A', 'B', 'C', 'D'):
                if srcRoomId == amphipod: continue
                src, srcEntrance = roomRemovePoint(mapStr, srcRoomId)
                if src and mapStr[src] == amphipod:
                    sources.append((src, srcEntrance))

            # Add any matching apmphipods from the hallway
            sources += map(lambda x : (x, x),
                           filter(lambda x : mapStr[x] == amphipod, range(11)))

            for src, srcEntrance in sources:
                # Set [i:j] to the forward range excluding 'srcEntrance' and
                # 'destEntrance'
                if srcEntrance < destEntrance:
                    i, j = (srcEntrance + 1, destEntrance)
                else:
                    i, j = (destEntrance + 1, srcEntrance)
                # Check if path is clear from srcEntrance to dstEntrance
                if (mapStr[i:j] != emptyHall[i:j]): continue

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
    workQueue[mapStr] = cost

def popWorkQueue(workQueue):
    """Remove and return (as a tuple) the item from the `workQueue` having the
    smallest cost value"""
    key, value = min(workQueue.items(), key=lambda x : x[1])
    workQueue.pop(key)
    return (key, value)

def processWorkQueue(workQueue, memo):
    mapStr, cost = popWorkQueue(workQueue)  # Work on lowest cost map so far
    while mapStr != solution:
        showProgress(mapStr)
        orgMapStr = mapStr
        qlen = len(workQueue)
        for roomId in ('A', 'B', 'C', 'D'):
            src, srcHall = roomRemovePoint(mapStr, roomId)
            if not src: continue
            for dest in range(srcHall - 1, -1, -1):
                if mapStr[dest] != '.': break
                addNextMove(mapStr, cost, src, dest, workQueue, memo)
            for dest in range(srcHall + 1, len(emptyHall)):
                if mapStr[dest] != '.': break
                addNextMove(mapStr, cost, src, dest, workQueue, memo)
        mapStr, cost = popWorkQueue(workQueue)
    showProgress(mapStr)
    print('')
    return cost

def solve(strMap):
    return processWorkQueue( {strMap : 0 }, {} )

def readMap(infile):
    it = iter(infile)
    line = next(it)
    assert(line == "#############\n")
    line = next(it)
    assert(line == "#...........#\n")
    mapStr = emptyHall
    line1 = next(it)
    line2 = "  #D#C#B#A#"
    line3 = "  #D#B#A#C#"
    line4 = next(it)
    for roomId in ('A', 'B', 'C', 'D'):
        src, srcHall = mapEncoding[roomId]
        for line in (line1, line2, line3, line4):
            mapStr += line[srcHall + 1]
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
    for i in range(1,4):
        print("  #{}#{}#{}#{}#".format(mapStr[mapEncoding['A'][0] + i],
                                       mapStr[mapEncoding['B'][0] + i],
                                       mapStr[mapEncoding['C'][0] + i],
                                       mapStr[mapEncoding['D'][0] + i]))
    print("  #########")

def progress(mapStr):
    ret = 0
    ret += len(re.compile(r'(.*[^A])?(A*)').fullmatch(mapStr, 11, 15).group(2))
    ret += len(re.compile(r'(.*[^B])?(B*)').fullmatch(mapStr, 15, 19).group(2))
    ret += len(re.compile(r'(.*[^C])?(C*)').fullmatch(mapStr, 19, 23).group(2))
    ret += len(re.compile(r'(.*[^D])?(D*)').fullmatch(mapStr, 23, 27).group(2))
    return ret

bestProgress = 0
def showProgress(mapStr):
    global bestProgress
    prog = progress(mapStr)
    if prog >= bestProgress:
        bestProgress = prog
        print(f"\rProgress of %s = %2d/16" % (mapStr, prog), end='')

infile = open("puzzle23_input.txt", "r")
mapStr = readMap(infile)
printMap(mapStr)
energy = solve(mapStr)
print("Min energy =", energy)
