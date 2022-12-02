class Range(tuple):
    def __new__(cls, min, max = None):
        if max is None: max = min
        assert(isinstance(min, int) and isinstance(max, int) and min <= max)
        return super().__new__(cls, (min, max))

    def min(self):
        return self[0]

    def max(self):
        return self[1]

x = Range(0, 10)
print(x)

print(x.min(), x.max())

a, b = x
print(a, b)
