# Advent of Code day 20, part 2
# Image enhancement algorithm run 50 times

import numpy as np

# Placevalues for 9 binary digits
placeValues = np.array([ 256, 128, 64, 32, 16, 8, 4, 2, 1 ])

def pad(image, padVal):
    ### Surround image with two rows and columns of `padVal`:
    (rows, cols) = image.shape
    padRow = np.array([ padVal ] * cols)
    paddedImage = np.vstack((padRow, padRow, image, padRow, padRow))
    rows += 4
    padCol = np.array( [ [ padVal ] ] * rows  )
    paddedImage = np.hstack((padCol, padCol, paddedImage, padCol, padCol))
    return paddedImage

# `algorithm` is a 1-D np array of 0 and 1.
# `image` is a 2-D np array of 0 and 1.
def enhance(algorithm, image):
    """Return enhanced image"""

    outrows, outcols = image.shape
    outrows -= 2
    outcols -= 2
    result = np.ndarray(shape = (outrows, outcols), dtype = int)
    for x in range(outrows):
        for y in range(outcols):
            bits9 = image[x:x+3, y:y+3].reshape((9,))
            windowVal = (bits9 * placeValues).sum()
            result[x, y] = algorithm[windowVal]

    return result

def hashDotsToBinary(hashDots):
    """Convert a string of '#' and '.' characters into a tuple of 1 and 0
    integer values, respectively."""
    return tuple(map(lambda c : 1 if c == '#' else 0, hashDots.rstrip()))

infile = open("puzzle20_input.txt", "r")

inIter = iter(infile)
algorithm = hashDotsToBinary(next(inIter))
# print("algorithm =", algorithm)

assert('\n' == next(inIter))  # Skip blank line

image = np.array( [ hashDotsToBinary(next(inIter)) ]) # Read first row of image

# Read rest of image, adding a row for each line
for line in inIter:
    image = np.vstack((image, hashDotsToBinary(line)))

# print("input image = \n", image)

padVal = 0
for rep in range(50):
    image = enhance(algorithm, pad(image, padVal))
    padVal = algorithm[0 if padVal == 0 else 511]

print("Final image size =", image.shape)
print("Total lit pixels =", image.sum())
