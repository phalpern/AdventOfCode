# Advent of Code day 16, part 2
# Evaluate packets

# Represent a string of hexidecimal digits as a stream of binary digits, with a
# cursor that advances through them.
class BitStream:
    def __init__(self, hexstring):
        self.cursor     = iter(hexstring)  # iterator through hex string
        self.position   = 0  # Position from start (in bits)
        self.decoded    = 0  # Bits that have been decoded into integer form
        self.numDecoded = 0  # Number of bits that have been decoded

    # Return the next `n` bits as an integer
    def getBits(self, n):
        numDecoded = self.numDecoded
        decoded    = self.decoded

        # print("n = {}, numDecoded = {}, ".format(n, numDecoded), end='')
        if n > numDecoded:
            bitsNeeded = (n - numDecoded + 3) & ~3  # Round up to 4 bit units
            nibblesNeeded = bitsNeeded >> 2
            # print("bitsNeeded = {}, nibblesNeeded = {}, ".format(bitsNeeded, nibblesNeeded), end='')
            # Read hex number of `nibblesNeeded` length
            nibbles = ''
            for i in range(nibblesNeeded):
                nibbles += next(self.cursor)
            decoded = (decoded << bitsNeeded) + int(nibbles, 16)
            numDecoded += bitsNeeded

        remainingBits = numDecoded - n  # Low-order bits not used in result
        ret = decoded >> remainingBits  # Compute result

        # Keep only the remaining bits
        self.decoded    = decoded & ((1 << remainingBits) - 1)
        self.numDecoded = remainingBits

        self.position += n
        # print("ret = ", ret)
        return ret

# Map opcodes to binary operations
opcodes = {
    0 : lambda a, b : a + b,
    1 : lambda a, b : a * b,
    2 : lambda a, b : a if a < b else b,
    3 : lambda a, b : a if b < a else b,
    5 : lambda a, b : a > b,
    6 : lambda a, b : a < b,
    7 : lambda a, b : a == b
    }

class Packet:
    version : 0
    type    : 0
    value   : None

    # Read a series of 5-bit values discarding the high bit of each, and
    # treating the remaining 4 bits as the next 4 bits in an integer
    # value. The first value with a high bit of 0 is the last value in the
    # stream of 4-bit chunks.
    def readLiteral(stream):
        result = 0
        chunk = stream.getBits(5)
        while chunk & 0x10:
            result = (result << 4) + (chunk & 0x0F)
            chunk = stream.getBits(5)
        result = (result << 4) + chunk
        return result

    def __init__(self, stream):
        self.version = stream.getBits(3)
        self.type    = stream.getBits(3)

        if self.type == 4:
            self.value = Packet.readLiteral(stream)
        else:
            lentypeId = stream.getBits(1)

            self.value = [ ]  # Value is a list of subpackets
            if lentypeId == 0:
                totalSubpacketLen = stream.getBits(15)
                startpos = stream.position
                # Recursively read packets until `totalSubpacketLen` bits are
                # consumed
                while stream.position < startpos + totalSubpacketLen:
                    self.value.append(Packet(stream))
                assert(stream.position == startpos + totalSubpacketLen)
            else:
                numSubpackets = stream.getBits(11)
                # Recursively read packets until `numSubpackets` bits are read
                for i in range(numSubpackets):
                    self.value.append(Packet(stream))

    def __repr__(self):
        return "< {}, {}, {} >".format(self.version, self.type, self.value)

    def eval(self):
        if self.type == 4:  # Literal
            return self.value
        op = opcodes[self.type]
        valIter = iter(self.value)
        ret = next(valIter).eval()
        for v in valIter:
            ret = op(ret, v.eval())
        return ret

infile = open("puzzle16_input.txt", "r")

for hexstr in infile:
    print(hexstr, end='')
    bs = BitStream(hexstr.rstrip())
    packet = Packet(bs)
    print(packet)
    print("Evaluate to", packet.eval())
