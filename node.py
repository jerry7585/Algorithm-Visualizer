class Node():
    def __init__(self, parent, position):
        self.parent = parent
        self.position = position

        self.g = 0  # used to store the cost of reaching this node from the starting point
        self.h = 0  # used to store the heuristic (estimated) cost of reaching the goal node from this node
        self.f = 0  # sum of g and h and represents the estimated total cost of the path through this node

    def __eq__(self, other):
        return self.position == other.position