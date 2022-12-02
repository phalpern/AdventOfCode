# Mutating iterator module

class MutatingIteratorImp:
    def __init__(self, mi):
        self.mutatingIter = mi

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.mutatingIter)

class MutatingIterator:
    def __init__(self, lst):
        self.theList = lst
        self.index   = 0     # one past the item last returned by __next__

    def __iter__(self):
        return MutatingIteratorImp(self)

    def __next__(self):
        if self.index < len(self.theList):
            self.index += 1
            return self.theList[self.index - 1]
        else:
            raise StopIteration

    def get_list(self):
        """Returns the list being iterated on."""
        return self.theList

    def append(self, val):
        """Appends to the *end* of the list. This call has no effect on the
        current position. If the current position was previously at the end of
        the list, then the next call to `__next__` will return the newly
        inserted item."""
        self.theList.append(val)

    def insert(self, val):
        """Inserts `val` before the current position. The newly inserted item
        will not be iterated over."""

        self.theList.insert(self.index - 1, val)
        self.index += 1

    def insert_after(self, val):
        """Inserts `val` after the current position. The newly inserted item
        will be seen next in the iteration order."""

        self.theList.insert(self.index, val)

    def insert_at(self, index, val):
        """Inserts `val` at the specified `index`.  If `index` is after the
        current position, then `val` will eventually be iterated over;
        otherwise it will not."""

        self.theList.insert(index, val)
        if index < 0:
            index += len(self.theList)
        if index <= self.index - 1:
            self.index += 1

    def remove(self, n = 1):
        """Removes `n` elements (default 1) at the current position.
        The current item is invalidated.  Iteration resumes after the last
        deleted element."""

        index = self.index - 1
        for i in range(n):
            self.theList.pop(index)
        self.index -= n

    def skip_to(self, pos):
        """Skip to a specified position. `pos` is the index of the next
        element to be traversed."""

        self.index = pos;

    def skip(self, n = 1):
        """Skips the next `n` elements (default 1) in the iteration
        sequence.  If `n` is negative, then goes backwards in the iteration
        sequence."""

        self.skip_to(self.index + n)

    def skip_rest(self):
        """Skip the remaining elements in the iteration sequence."""

        self.skip_t(len(self.theList))

    def restart(self):
        """Restart the iteration from the beginning"""

        self.skip_to(0)

def test():
    myList = list(range(10))
    mi = MutatingIterator(myList)

    for v in mi:
        print(v)
        if 0 == v % 3:
            mi.insert(-v)
        if v > 5:
            mi.insert_after(v - 100)
        if v == -92:
            mi.remove()
            mi.insert_at(2, -92)
            mi.insert_at(-1, 2)

    print(myList)

# test()
