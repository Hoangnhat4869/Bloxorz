from __future__ import annotations
from blockMove import Block, Direction


class BNode:

    def __init__(self, block: Block):
        self.block = block
        self.left = None
        self.right = None
        self.up = None
        self.down = None
        self.spacebar = None

        # for display
        self.dir_from_parent = None
        self.parent = None

        # for a-star search
        self.f_cost = 0  # g + h cost

        # for Monte Carlo Tree search
        self.children = list()
        self.visits = 0
        self.score = 0

    def add_child(self, child: BNode):
        self.children.append(child)

    def update(self, score: int):
        self.score += score
        self.visits += 1

    def __lt__(self, other: BNode):
        """
        Compare one treenode to another by f_cost, used to build a min-heap.
        :param other: Tree Node
        :return: True if current node has lower f_cost than other, False otherwise.
        """
        return self.f_cost < other.f_cost

    def __str__(self):
        """
        String representation.
        :return: Formatted string of object attributes values.
        """
        dir_name = self.dir_from_parent.name.lower() if self.dir_from_parent else "none"
        parent_hash = hash(self.parent) if self.parent else "none"

        return '[hash(Node): {}, hash(Parent): {}, Parent->{:5s}]'.format(
            hash(self), parent_hash, dir_name)