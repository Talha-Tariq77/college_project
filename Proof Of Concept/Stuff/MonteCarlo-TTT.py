game_tree = [[]]

class Node:
    def __init__(self, game_tree, state, parent, children, value=(0, 0)):
        self.root = None
        self.parent = parent
        self.children = children
        self.value = value  # q/Q = wins/ vists
        self.state = state
        self.UCT = None
        self.depth = None

        if self.parent is None:
            self.depth = 0
            self.root = True
        else:
            self.depth = self.parent.depth + 1
            self.root = False


        self.add_to_game_tree(game_tree)

    def add_to_game_tree(self, game_tree):
        if not len(game_tree) > self.depth:
            game_tree[self.depth] = []

        game_tree[self.depth].append(self)

    def __repr__(self):
        # return '{}, {}'.format(self.value)
        return str(self.value)

    def display_node(self):
        for row in self.state:
            for pos in row:
                if pos == ' ':
                    print('☐', end='')
                else:
                    print(pos, end='')
            print()

    def print_lineage(self):
        current_node = self
        while current_node.parent is not None:
            current_node.parent.display_node()
            print(current_node.parent)
            current_node = current_node.parent