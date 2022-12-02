# Advent of Code day 10, part 1
# Score the autocompletes on incomplete input lines

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

autocompletePoints = {
    '(' : 1,
    '[' : 2,
    '{' : 3,
    '<' : 4
    }

# Return the autocomplete score for the current line by popping the stack.
def autocomplete():
    score = 0
    while len(stack) > 1:
        c = stack.pop()
        score = score * 5 + autocompletePoints[c]
    return score

infile = open("puzzle10_input.txt", "r")

corrupt = 0
incomplete = 0
points = [ ]
for line in infile:
    clearStack()
    for c in line.rstrip():
        if not consume(c):
            # Corrupt line
            corrupt += 1
            clearStack()
            break
    if len(stack) > 1:
        incomplete += 1
        points.append(autocomplete())

assert(len(points) & 1)
points.sort()
med = points[len(points) >> 1]

print("Found {} incomplete lines with median {} points".format(incomplete, med))
