# Advent of code day 21, part 2
# Quantum Dirac dice

# Rolling 3, 3-sided Dirac dice yields 27 universes but only 7 outcomes for the
# total of the 3 dice (3-9).  Thus many of the universes have the same
# outcome. Using this knowledge, we can simulate the game with a tree of degree
# 7 instead of degree 27, keeping count of the number of identical universes
# using this array.
#
# Dice total  =   0, 1  2  3  4  5  6  7  8  9
DiceUniverses = [ 0, 0, 0, 1, 3, 6, 7, 6, 3, 1 ]

# Tuple of starting positions for player0 and player1, respectively
startpos_test = (4, 8)
startpos_real = (8, 5)

startpos = startpos_real

winningScore = 21

def advance(playerState, roll):
    pos, score = playerState
    pos = (pos - 1 + roll) % 10 + 1
    score += pos
    return (pos, score)

def addToStateMap(stateMap, thisPlayer, otherPlayer, universes):
    key = (thisPlayer, otherPlayer)
    universes += stateMap.get(key, 0)
    stateMap[key] = universes

winningUniverses = [ 0, 0 ]
def playturn(playerId, gameStateMap):
    global winningUniverses
    otherPlayerId = 1 - playerId
    newStateMap = { }
    for playerStates, universes in gameStateMap.items():
        thisPlayer, otherPlayer = playerStates
        for roll in range(3, 10):
            nextState = advance(thisPlayer, roll)
            nextUniverses = universes * DiceUniverses[roll]
            if nextState[1] >= winningScore:
                winningUniverses[playerId] += nextUniverses
            else:
                addToStateMap(newStateMap, otherPlayer, nextState, nextUniverses)
    return newStateMap

def play(startPos):
    gameStateMap = { ((startPos[0], 0), (startPos[1], 0)) : 1 }
    whoseTurn = 0
    turn = 1
    while gameStateMap:
        gameStateMap = playturn(whoseTurn, gameStateMap)
        print("turn {}, {} states".format(turn, len(gameStateMap)))
        turn += 1
        whoseTurn = 1 - whoseTurn

play(startpos)

print("Player 0 wins in {} universes".format(winningUniverses[0]))
print("Player 1 wins in {} universes".format(winningUniverses[1]))
