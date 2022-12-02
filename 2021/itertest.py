class BackRange:
    def __init__(self, size):
        self.sz = size

    def __iter__(self):
        return range(self.sz, 0, -1).__iter__()

for i in BackRange(5):
    print(i)
