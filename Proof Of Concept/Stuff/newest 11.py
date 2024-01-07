import math
import random

game_tree = {0: []}


class Node:
    def __init__(self, parent, children, state=None, UCT=None, root=False):
        self.parent = parent
        self.children = children
        self.value = (0, 0)  # q/Q = wins/ vists
        self.state = state
        self.root = root
        if root:
            self.depth = 0
        else:
            self.depth = self.parent.depth + 1
        self.add_to_game_tree()

    def add_to_game_tree(self):
        if not self.root:
            if not len(game_tree) > self.depth:
                game_tree[self.parent.depth + 1] = []
        game_tree[self.depth].append(self)

    def __repr__(self):
        return '{}, {}, {}'.format(self.state, self.value, self.depth)  # self.parent is repr'd here

    def display_node(self):
        for row in self.state:
            for pos in row:
                if pos == ' ':
                    print('☐', end='')
                else:
                    print(pos, end='')
            print()
        print(self)

        # def print_lineage(self):
        #     node = self
        #     print(node)
        #     while node.parent != None:
        #         print(node.parent)
        #         node = node.parent
        #     else:
        #         print(node)


game_state = [[' ', ' ', ' '],
              [' ', ' ', ' '],
              [' ', ' ', ' ']]
# results = []

root = Node(parent=None, children=[], state=game_state, root=True)


class MonteCarlo:
    def __init__(self, grid, player=1):
        self.local_grid = grid
        self.symbols = ['X', 'O']
        self.player = player
        self.C = 1
        self.iterate = 100
        self.count = 1
        if self.player == 1:
            self.human = 0
        else:
            self.human = 1

    def get_UCT(self, node):
        if node.parent != None:
            W = node.value[0]
            n = node.value[1]
            N = node.parent.value[1]
            if n == 0:
                return math.inf
            else:
                return W / n + (self.C * math.sqrt(math.log(N) / n))
        else:
            return math.inf

    def select(self, node):
        UCT_maximum = 0
        UCT_maximiser = None
        if node.children:
            for child_node in node.children:
                if self.get_UCT(child_node) > UCT_maximum:
                    UCT_maximum = self.get_UCT(child_node)
                    UCT_maximiser = child_node
            return UCT_maximiser
        else:
            return node

    def check_move(self, grid, coordinate):
        x, y = coordinate
        if grid[y][x] != ' ':
            return False
        else:
            return True

    def get_children(self, node):
        for x in range(3):
            for y in range(3):
                if self.check_move(node.state, (x, y)):
                    new_child = Node(node, [])
                    new_child.state = [x[:] for x in node.state]
                    new_child.state[y][x] = self.symbols[self.count % 2]
                    node.children.append(new_child)

    def expand(self, node):
        self.get_children(node)
        return random.choice(node.children)

    def simulate(self, selected_node):
        self.get_children(selected_node)
        copy_node = selected_node
        while len(copy_node.children) > 0:
            copy_node = random.choice(copy_node.children)
            self.get_children(copy_node)
        W1, n1 = selected_node.value
        W2, n2 = self.check_win(copy_node.state)
        selected_node.value = (W1 + W2, n1 + n2)

    def back_propagate(self, simulated_node):
        while simulated_node.parent != None:
            W1, n1 = simulated_node.parent.value
            W2, n2 = simulated_node.value
            simulated_node.parent.value = (W1 + W2, n1 + n2)
            simulated_node = simulated_node.parent

    def Monte_Carlo(self):
        while self.count <= self.iterate:
            selected_leaf = self.select(game_tree[0][0])  # starts selection with root, returns the selected leaf
            if selected_leaf.value[1] == 0:  # if node hasn't been visited
                self.simulate(selected_leaf)  # simulate a game from the node and back propagate it
                self.back_propagate(selected_leaf)
            else:
                simulation_node = self.expand(selected_leaf)
                self.simulate(simulation_node)
                self.back_propagate(simulation_node)
            self.count += 1
        move_node = self.make_move()
        move_node.display_node()
        return move_node

    def make_move(self):
        simulation_max = 0
        move_node = None
        for node in game_tree[1]:
            if node.value[1] > simulation_max:
                simulation_max = node.value[1]
                move_node = node
        return move_node

    def get_winners(self, grid):
        winners = []
        # horizontal
        for x in range(len(grid)):
            winners.append(grid[x])

        # vertical
        for y in range(len(grid[0])):
            col = []
            for row in range(len(grid)):
                col.append(grid[row][y])
            winners.append(col)

        right_down = []
        left_down = []

        for y in range(len(grid)):
            for x in range(len(grid[y])):
                if y == x:
                    right_down.append(grid[y][x])
                if y == -x + 2:
                    left_down.append(grid[y][x])
        winners.append(right_down)
        winners.append(left_down)
        return winners

    def board_filled(self, grid):
        for row in grid:
            if ' ' in row:
                return False
        return True

    def check_win(self, grid):
        for row in self.get_winners(grid):
            if row == [self.symbols[self.player - 1]] * 3:
                return 1, 1  # WIN
            elif row == [self.symbols[self.player - 2]] * 3:
                return 0, 1  # LOSS
        if self.board_filled(grid):
            return 0.5, 1  # DRAW


# game tree cannot be changed within a function
# because it is in a different scope

class Game:
    def __init__(self):
        self.game_tree = game_tree
        start_state = [[' ', ' ', ' '],
                       [' ', ' ', ' '],
                       [' ', ' ', ' ']]
        self.game_state = start_state
        self.mont = MonteCarlo(self.game_state)
        self.mont = MonteCarlo(game_state)
        self.human_player = 2

    def run(self):
        new_state = mont.Monte_Carlo()
        player_move = input('Move: ')
        new_state.state[int(player_move[0])][int(player_move[1])] = 'X'


mont = MonteCarlo(game_state)
new_state = mont.Monte_Carlo()
for i in range(3):
    player_move = input('Move: ')
    print(new_state)
    new_state.state[int(player_move[0])][int(player_move[1])] = 'X'

    game_tree = {0: []}
    Node(parent=None, children=[], state=new_state.state, root=True)
    mont.__init__(new_state.state)
    new_state = mont.Monte_Carlo()

    # Make game:
    # - prevent overlapping
    # - check wins
    # - reset and restart game_tree
    # - whatever needed for turns



    # move = input('Move [0,1,2 * 2]: ')
    # movex, movey = move
    # movex = int(movex)
    # movey = int(movey)
    # new_state.state[movex][movey] = 'X'
    #
    # new_state.display_node()
    # game_tree = {0: []}
    # root = Node(parent=None, children=[], state=new_state.state, root=True)
    # mont = MonteCarlo(new_state)
    # new_state = mont.Monte_Carlo()
    # new_state.display_node()