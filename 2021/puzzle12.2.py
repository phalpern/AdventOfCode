# Advent of Code day 12, part 2
# How many paths, visiting at most one small cave twice?

# The cave system is a graph. Represent the graph as a dictionary mapping each
# node (cave) to a list of edges (tunnels), where each edge is the name of
# another node.

# If this implementation seems like overkill, it's because I was experimenting
# with both iterators and linked lists in Python.

# Representation of a path (or partial path) through the graph.
class Path:
    # Representation is a linked list. The `node` member is a tuple, `(val,
    # link)` where `val` is the node ID string and `link` is the rest of the
    # path. The list is in reverse order, so `node` refers to the last node in
    # the path and "start" is the ID of the last node in the linked list.
    node : None

    # Iterate (in reverse order) over the values in the path
    class Iterator:

        path : None

        def __init__(self, path):
            self.path = path

        def __iter__(self):
            return self

        def __next__(self):
            if self.path == None:
                raise StopIteration
            else:
                val = self.path.lastValue()
                self.path = self.path.node[1]
                return val

    def __init__(self, val, link=None):
        self.node = (val, link)

    def __iter__(self):
        return Path.Iterator(self)

    # Represent the path as a list (in forward order)
    def __repr__(self):
        result = ""
        for val in self:
            comma = ',' if result else ''
            result = str(val) + comma + result
        return result

    # Return `True` if `val` exists in this path; else `False`
    def hasValue(self, val):
        for v in self:
            if val == v:
                return True
        return False

    # Return the last value in the path
    def lastValue(self):
        return self.node[0]

# Read a graph, where each line represents an edge in the form 'cave1-cave2'.
# The graph is represented as a dictionary mapping a cave name (the key) to a
# list of adjacent caves (the value) reachable from that cave in one step.
def readGraph(infile):
    graph = { }
    for edge in infile:
        cave1, cave2 = edge.rstrip().split('-')
        # Add edges in both directions
        if cave1 in graph:
            graph[cave1].append(cave2)
        else:
            graph[cave1] = [ cave2 ]

        if cave2 in graph:
            graph[cave2].append(cave1)
        else:
            graph[cave2] = [ cave1 ]
    return graph

# Recursively visit all caves reachable from `path` using the rules for cave
# traversal.  Return the number of paths found that terminate at the the "end"
# cave.  `revisitSmall` is true if you are allowed to visit a small cave again.
depth=0
def visitPaths(graph, path, revisitSmall=True):
    global depth
    depth += 1
    if depth > 20:
        print("recursion exceeds 20 for path: ", path)
        print("Graph = ", graph)
        raise AssertionError
    endCount = 0  # Number of complete paths found
    cave = path.lastValue()
    for adjacent in graph[cave]:
        if adjacent == "end":
            endCount += 1
            path = Path(adjacent, path)
            # print("Found path: ", path)
        elif adjacent == "start":
            pass
        # Large caves have upper-case names; small caves have lowercase names.
        # Large cave; visit even if visited before on this path
        # Small cave; visit only if not visited before on this path and
        # `revisitSmall` is True (meaning that a small cave was already visited
        # twice).
        elif adjacent.isupper() or not path.hasValue(adjacent):
            endCount += visitPaths(graph, Path(adjacent, path), revisitSmall)
        elif revisitSmall:
            endCount += visitPaths(graph, Path(adjacent, path), False)
    depth -= 1
    return endCount

infile = open("puzzle12_input.txt", "r")

graph = readGraph(infile)
count = visitPaths(graph, Path("start"))

print("Found {} paths".format(count))
