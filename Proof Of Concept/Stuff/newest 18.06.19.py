import math
import random

game_tree = {0: []}

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
    def __init__(self, game_tree, parent, children, state=None, UCT=None, root=False):
        self.game_tree = game_tree
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
            if not len(self.game_tree) > self.depth:
                self.game_tree[self.parent.depth + 1] = []
        self.game_tree[self.depth].append(self)

    def __repr__(self):
        # return '{}, {}'.format(self.value)  # self.parent is repr'd here
        return str(self.value)

    def display_node(self):
        for row in self.state:
            for pos in row:
                if pos == ' ':
                    print('☐', end='')
                else:
                    print(pos, end='')
            print()


        # print(self)

    # def print_lineage(self):
    #     node = self
    #     print(node)
    #     while node.parent != None:
    #         print(node.parent)
    #         node = node.parent
    #     else:
    #         print(node)


# game_state = [[' ', ' ', ' '],
#               [' ', ' ', ' '],
#               [' ', ' ', ' ']]
# results = []


class MonteCarlo:
    def __init__(self, grid, game_tree, player=1, first=1):
        self.game_tree = game_tree
        Node(self.game_tree, parent=None, children=[], state=grid, root=True)
        self.local_grid = grid
        self.symbols = ['X', 'O']
        self.player = player
        self.C = 2**0.5
        self.iterate = 1000
        self.count = first
        self.human = xor(self.player)

    def get_UCT(self, node):
        if node.parent != None:
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
        self.get_children(selected_node, get_turn(selected_node.state, self.symbols))
        copy_node = selected_node
        while len(copy_node.children) > 0:
            copy_node = random.choice(copy_node.children)
            self.get_children(copy_node, get_turn(copy_node.state, self.symbols))
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
            selected_leaf = self.select(self.game_tree[0][0])  # starts selection with root, returns the selected leaf
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
        possibles = sorted(game_tree[depth], key=lambda node: node.value[1], reverse=True)
        for row in range(3):
            for state in possibles:
                for val in state.state[row]:
                    if val == ' ':
                        val = '☐'
                    print(val, end='')
                print('   ', end='\t\t\t')
            print()
        print()
        for state in possibles:
            print(state.value, end='\t\t')
        print()




# game tree cannot be changed within a function
# because it is in a different scope

class Game:
    def __init__(self, game_tree):
        start_state = [[' ', ' ', ' '], # need to add root, not do this
                      [' ', ' ', ' '],
                      [' ', ' ', ' ']]
        self.game_state = start_state
        self.mont = MonteCarlo(self.game_state, game_tree, player=random.randint(0, 1))
        self.human_player = 2
        self.turn = 1
        self.result = None
        self.wins = (0, 0)  # comp, h
        self.comp_order = 1 #random.randint(0, 1)
        self.game_node = None
    # deal with this.

    def player_turn(self):
        coordinates = input("Move: ")
        self.game_node.state = coordinates

    def run(self):
        while self.result == None:
            self.mont.game_tree[0][0].display_node()

            if self.turn % 2 == self.comp_order:
                print("Computer Turn")
                self.game_node = self.mont.Monte_Carlo()
                print('turn', self.turn)

                self.mont.display_game_tree(self.turn)
                # self.mont.__init__(self.game_state, {0: []}) moved this to 308

            elif self.turn % 2 == xor(self.comp_order):
                print("Human Turn")
                human_move = input("Coordinates: ")
                while not self.handle_input(human_move):
                    print("Error: Invalid Coordinate")
                    human_move = input("Coordinates: ")
                x, y = input_convertor(human_move)
                self.game_node.state[x][y] = 'X'

            self.mont.__init__(self.game_node.state, {0: [self.game_node]})

            self.result = self.mont.check_win(self.game_node.state)

            self.turn += 1

        self.mont.game_tree[0][0].display_node()

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



#a = Node(game_tree, None, [], root=True, state=[['O', ' ', ' '],
#                                                [' ', ' ', ' '],
#                                                [' ', ' ', ' ']])
game = Game(game_tree)
#print(a, a.state)
#game.mont.get_children(a)
game.run()



# def count_places(x):
#     count = 0
#     for row in x:
#         for symb in row:
#             if symb == ' ':
#                 count += 1
#     return count

# working alternative code:
#
# mont = MonteCarlo(game_state, game_tree)
# new_state = mont.Monte_Carlo()
#
# turn = 1
# while mont.check_win(new_state.state) == None:
#     turn += 1
#     if turn % 2 == 0:
#         player_move = input('Move: ')
#         new_state.state[int(player_move[0])][int(player_move[1])] = 'X'
#         new_state.display_node()
#     elif turn % 2 == 1:
#         if count_places(new_state.state) > 1:
#             game_tree = {0: []}
#             Node(parent=None, children=[], state=new_state.state, root=True)
#             mont.__init__(new_state.state, game_tree)
#             print('final', new_state)
#             new_state = mont.Monte_Carlo()
#         else:
#             new_state[new_state.state.index(' ')] = 'O'

# final_state = [['X', 'O', 'O'],
#                ['O', 'O', 'X'],
#                ['X', 'X', ' ']]
#
#
# mont = MonteCarlo(final_state, game_tree)
# print(mont.check_move(final_state, (2, 2)))


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

# display game tree
# check each part individually

# add coin/ different starting player
# check if sequence is best it could be
# finish off single tic tac toe
# make it all work with ultimate tic tac toe
# - data storage
# - Inputs
# - check AI
#  add on to sequence anything good

