# Advent of Code day 10, part 1
# Score for syntax errors on corrupted lines

# String of chunk delimiters.
# Even-indexed characters start chunks, odd-indexed ones end
# chunks. Chunk-starting characters immediately precede their corresponding
# chunk-ending character.
chunkDelimiters = "()[]{}<>"

stack = [ ]  # Parse stack

# Clear the stack.
def clearStack():
    global stack
    stack = [ 'x' ]  # Never empty. Popping the 'x' will result in a parse error

# Consume the specified character. Return True if success, False on syntax error
def consume(c):
    global stack
    delimiterPos = chunkDelimiters.find(c)
    if delimiterPos < 0:
        return False
    elif delimiterPos & 1:
        # Odd position; closing delimiter
        match = stack.pop()
        return (chunkDelimiters[delimiterPos - 1] == match)
    else:
        stack.append(c)
        return True

delimiterPoints = {
    ')' : 3,
    ']' : 57,
    '}' : 1197,
    '>' : 25137
    }

infile = open("puzzle10_input.txt", "r")

corrupt = 0
points = 0
for line in infile:
    clearStack()
    for c in line.rstrip():
        if not consume(c):
            # Corrupt line
            corrupt += 1
            points += delimiterPoints[c]
            break

print("Found {} corrupt lines totalling {} points".format(corrupt, points))
