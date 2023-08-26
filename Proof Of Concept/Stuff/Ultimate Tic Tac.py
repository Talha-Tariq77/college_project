import math
import random

def tuple_conv(tup):
    """Input: Tuple, Output: Printable string of tuple"""
    x, y = tup
    if x == 0.5:
        x = 5
    return str(x) + ' ' + str(y)

def get_turn(state, symbs):
    x = 0
    o = 0
    for row in state:
        for symb in row:
            if symb == 'X':
                x += 1
            elif symb == 'O':
                o += 1
    if x > o:
        return 1
    elif o > x:
        return 0
    elif x + o == 9:
        return 'STOP'
    else:
        return 1

def display_game_tree(game_tree, x):
    print()
    level = game_tree[x]
    for node in level:
        node.display_node()
        print(node)


def input_convertor(number):
    number = int(number)
    x, y = None, None
    conv = [[7, 8, 9], [4, 5, 6], [1, 2, 3]]
    for row in conv:
        if number in row:
            x = conv.index(row)
            y = row.index(number)
    return (x, y)


def xor(dig):
    if dig == 1:
        return 0
    else:
        return 1


class Node:
    def __init__(self, game_tree, parent, children, state=None, root=False, value=(0,0)):
        # self.game_tree = game_tree
        self.parent = parent
        self.children = children
        self.value = value  # q/Q = wins/ vists
        self.state = state
        self.root = root
        if root:
            self.depth = 0
        else:
            self.depth = self.parent.depth + 1
        self.add_to_game_tree(game_tree)

    def make_root(self):
        self.root = True
        self.depth = 0
        self.parent = None
        self.children = []

    def add_to_game_tree(self, game_tree):
        if not self.root:
            if not len(game_tree) > self.depth:
                game_tree[self.parent.depth + 1] = []
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


class MonteCarlo:
    def __init__(self, grid, game_tree, player=1, first=1):
        self.game_tree = game_tree
        self.root = Node(self.game_tree, parent=None, children=[], state=grid, root=True)
        self.local_grid = grid
        self.symbols = ['X', 'O']
        self.player = player
        self.C = 2 ** 0.5  # Try changing C value
        self.iterate = 1000
        self.count = first
        self.human = xor(self.player)

    def get_UCT(self, node):
        if node.parent is not None:
            W = node.value[0]
            n = node.value[1]
            N = node.parent.value[1]
            if n == 0:
                return math.inf
            else:
                return W/n + (self.C * math.sqrt(math.log(N)/n))
        else:
            return math.inf

    def select(self, node):
        while len(node.children) > 0:
            UCT_maximum = 0
            UCT_maximiser = None
            for child_node in node.children:
                child_UCT = self.get_UCT(child_node)
                if child_UCT > UCT_maximum:
                    UCT_maximum = child_UCT
                    UCT_maximiser = child_node
            if UCT_maximiser is not None:
                node = UCT_maximiser
            else:
                node = random.choice(node.children)

        return node

        # UCT_maximum = 0
        # UCT_maximiser = None
        #
        # if node.children:
        #     for child_node in node.children:
        #         if self.get_UCT(child_node) > UCT_maximum:
        #             UCT_maximum = self.get_UCT(child_node)
        #             UCT_maximiser = child_node
        #     return UCT_maximiser
        # else:
        #     return node

    def check_move(self, grid, coordinate):
        x, y = coordinate
        if grid[y][x] != ' ':
            return False
        else:
            return True

    def get_children(self, node, player):
        if player in [1, 0]:
            for x in range(3):  # change this to simulate only in empty spaces
                for y in range(3):
                    if self.check_move(node.state, (x, y)):
                        new_child = Node(self.game_tree, node, [])
                        new_child.state = [x[:] for x in node.state]
                        new_child.state[y][x] = self.symbols[player]
                        # print()
                        # print(count % 2)
                        # print(new_child.state)
                        node.children.append(new_child)
            #print(node.children)  # provides good data

    def expand(self, node):
        self.get_children(node, self.count)
        if len(node.children) > 1:
            return random.choice(node.children)
        elif len(node.children) == 1:
            return node.children[0]

    def simulate(self, selected_node):
        """ need to edit this and the check_win and turn functions, to make sure they are using the right symbol
        on each iteration of the simulations etc.
        Need to make sure the AI doesnt choose the position which will cause it to lose, and always choses the position
        which will cause it to win in these simulations and in game.
        Make the choices in simulation and game not random, they should be the best for exploitation and
        exploration."""
        self.get_children(selected_node, get_turn(selected_node.state, self.symbols))
        copy_node = selected_node
        while len(copy_node.children) > 0:
            flag = True
            for node in copy_node.children:
                if self.check_win(node.state) == (1, 1):
                    copy_node = node
                    flag = False
            if flag:
                copy_node = random.choice(copy_node.children)
            self.get_children(copy_node, get_turn(copy_node.state, self.symbols))
        W1, n1 = selected_node.value
        W2, n2 = self.check_win(copy_node.state)
        selected_node.value = (W1 + W2, n1 + n2)

    def back_propagate(self, simulated_node):
        while simulated_node.parent is not None:
            W1, n1 = simulated_node.parent.value
            W2, n2 = simulated_node.value
            simulated_node.parent.value = (W1 + W2, n1 + n2)
            simulated_node = simulated_node.parent

    def Monte_Carlo(self):
        while self.count <= self.iterate:
            selected_leaf = self.select(self.game_tree[0][0])  # starts selection with root, returns the selected leaf
            # if self.check_win(selected_leaf.state) is not None:
                # selected_leaf.display_node()
                # print()
            if selected_leaf.value[1] == 0:  # if node hasn't been visited
                self.simulate(selected_leaf)  # simulate a game from the node and back propagate it
                self.back_propagate(selected_leaf)
            else:
                simulation_node = self.expand(selected_leaf)
                if not simulation_node:
                    break
                self.simulate(simulation_node)
                self.back_propagate(simulation_node)
            self.count += 1

        move_node = self.make_move()

        return move_node

    def make_move(self):
        simulation_max = 0
        move_node = None
        for node in self.game_tree[1]:
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
            if row == [self.symbols[self.player]] * 3:
                return 1, 1  # WIN
            elif row == [self.symbols[self.human]] * 3:
                return 0, 1  # LOSS
        if self.board_filled(grid):
            return 0.5, 1  # DRAW

    def display_game_tree(self, depth):

        possibles = sorted(self.game_tree[depth], key=lambda node: node.value[1], reverse=True)
        for row in range(3):
            for state in possibles:
                for val in state.state[row]:
                    if val == ' ':
                        val = '☐'
                    print(val, end='')
                print('', end='\t\t\t')
            print()
        print()
        for state in possibles:
            print(tuple_conv(state.value), end='\t\t\t')
        print()


# game tree cannot be changed within a function
# because it is in a different scope

class Game:
    def __init__(self, game_tree):
        start_state = [[' ', ' ', ' '], # need to add root, not do this
                      [' ', ' ', ' '],
                      [' ', ' ', ' ']]
        self.mont = MonteCarlo(start_state, game_tree, player=random.randint(0, 1))
        self.human_player = 2
        self.turn = random.randint(0, 1)
        self.result = None
        self.wins = (0, 0)  # comp, h
        self.game_node = self.mont.root

    def run(self):
        while self.result is None:
            self.mont.root.display_node()
            print('turn', self.turn)

            if self.turn == 1:
                print("Computer Turn")

                self.game_node = self.mont.Monte_Carlo()
                self.game_node.display_node()

                # for i in range(len(self.mont.game_tree)):
                #     print("Depth:", i)
                #     self.mont.display_game_tree(depth=i)
                #     b = [node for node in self.mont.game_tree[i] if node.value[1] != 0]
                #     print('visited', len(b), 'out of', len(self.mont.game_tree[i]))


                    #self.mont.display_game_tree(self.turn)

            elif self.turn == 0:
                print("Human Turn")

                human_move = input("Coordinates: ")
                while not self.handle_input(human_move):
                    print("Error: Invalid Coordinate")
                    human_move = input("Coordinates: ")

                x, y = input_convertor(human_move)
                self.game_node.state[x][y] = 'X'

            self.mont.__init__(self.game_node.state, {0: []})

            self.result = self.mont.check_win(self.game_node.state)

            self.turn = xor(self.turn)

        self.mont.root.display_node()

        self.endgame()

    def handle_input(self, coordinate):
        if coordinate not in [str(y) for y in list(range(10))]:
            return False
        x, y = input_convertor(coordinate)
        if self.game_node.state[x][y] != ' ':
            return False
        return True

    def endgame(self):
        if self.result == (1, 1):
            print("Computer Won!")
        elif self.result == (0, 1):
            print("Human Won!")
        else:
            print("Draw!")
        self.record()

    def record(self):
        file = open('record.txt', 'a')
        file.write(str(self.result[0]) + '\n')
        file.close()


def show_node(node):
    node.display_node()
    print(node)


game = Game({0: []})
game.run()


# starter = [['X', ' ', 'O'],
#            [' ', 'X', ' '],
#            [' ', ' ', ' ']]
#
# mont = MonteCarlo(starter, {0: []})
# pc_move_node = mont.Monte_Carlo()
# pc_move_node.display_node()
# print(pc_move_node)
#
# for i in range(len(mont.game_tree)):
#     print("Depth:", i)
#     print('All:')
#     mont.display_game_tree(depth=i)
#     print('\nVisited:')
#     b = [node for node in mont.game_tree[i] if node.value[1] != 0]
#     print('visited', len(b), 'out of', len(mont.game_tree[i]))
#
#     possibles = sorted(b, key=lambda node: node.value[1], reverse=True)
#     for row in range(3):
#         for state in possibles:
#             for val in state.state[row]:
#                 if val == ' ':
#                     val = '☐'
#                 print(val, end='')
#             print('', end='\t\t\t')
#         print()
#     print()
#     for state in possibles:
#         print(tuple_conv(state.value), end='\t\t\t')
#     print()
#
#     for state in possibles:
#         print(str(i) + ' ' + str(mont.game_tree[i].index(state)), end='\t\t\t')
#     print()
#
# print(mont.game_tree)
# print(len(mont.game_tree))
#
# a = input('Index of wanted: ')
# while a != 'exit':
#     i, n_index = a[0], a[1:]
#     mont.game_tree[int(i)][int(n_index)].print_lineage()
#     a = input('Index of wanted: ')






# mont.display_game_tree(2)
# print('len', len(mont.game_tree[2]), end='\n\n')
# print(len(mont.game_tree[len(mont.game_tree) - 1]))
# display_lineage(mont.game_tree[len(mont.game_tree) - 1][-1], mont.root)

# tree continues to expand nodes even after they have been won.

# display game tree
# check each part individually

# check if sequence is best it could be
# finish off single tic tac toe
# make it all work with ultimate tic tac toe0
# - data storage
# - Inputs
# - check AI
#  add on to sequence anything good

# Version checking:
# Look up History




# Make sure in simulation and game, when the winning (/losing aswell for simulation)
# move is available, it is always chosen.
