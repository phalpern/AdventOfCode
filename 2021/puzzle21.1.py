# Advent of code day 21, part 1
# Deterministic dice

class Die:
    """Deterministic 100-sided die"""
    nextRoll = 0  # Count 0-99, but add 1 before returning
    numRolls = 0  # How often was the die rolled

    def roll(self):
        r = self.nextRoll + 1
        self.nextRoll = r % 100
        self.numRolls += 1
        return r

class Player:
    """Player's position and score"""
    def __init__(self, playerNum, pos):
        self.playerNum = playerNum
        self.position = pos - 1  # Internal position is 0-9 instead of 1-10
        self.score    = 0

    def advance(self, num):
        self.position = (self.position + num) % 10
        self.score    += self.position + 1
        return self.score >= 1000

startpos_test = (4, 8)
startpos_real = (8, 5)

startpos = startpos_real

player1 = Player(1, startpos[0])
player2 = Player(2, startpos[1])

winner = None
loser  = None

die = Die()

while not winner:
    roll = die.roll() + die.roll() + die.roll()
    if player1.advance(roll):
        winner = player1
        loser  = player2
        break
    roll = die.roll() + die.roll() + die.roll()
    if player2.advance(roll):
        winner = player2
        loser  = player1
        break

print("winner = player{}, score = {}".
      format(winner.playerNum, winner.score))
print("loser  = player{},  score = {}".
      format(loser.playerNum, loser.score))
print("rolls = {}, loser score * rolls = {}".
      format(die.numRolls, die.numRolls*loser.score))
