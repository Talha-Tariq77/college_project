import math
import random
import time
from collections import Counter

def tuple_conv(tup):
    """Input: Tuple, Output: Printable string of tuple"""
    x, y = tup
    if x == 0.5:
        x = 5
    return str(x) + ' ' + str(y)


def find_turn(node, first):
    state = node.state
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
    else:
        return first


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
        self.UCT = None

        if root:
            self.depth = 0
            self.add_to_game_tree(game_tree)
        else:
            self.depth = self.parent.depth + 1

    def make_root(self):
        self.root = True
        self.depth = 0
        self.parent = None
        self.children = []

    def add_to_game_tree(self, game_tree):
        if not len(game_tree) > self.depth:
            game_tree[self.depth] = []

        game_tree[self.depth].append(self)

    def __repr__(self):
        #return str(self.value)
        return '{}, {}, {} UCT: {}, val: {}'.format(self.state[0], self.state[1], self.state[2], self.UCT, self.value)

    def display_node(self):
        for row in self.state:
            for pos in row:
                if pos == ' ':
                    print('☐', end='')
                else:
                    print(pos, end='')
            print()

    # def print_lineage(self):
    #     current_node = self
    #     while current_node.parent is not None:
    #         current_node.parent.display_node()
    #         print(current_node.parent)
    #         current_node = current_node.parent


class MonteCarlo:
    def __init__(self, grid, game_tree, player=1, first=1):
        self.game_tree = game_tree
        self.root = Node(self.game_tree, parent=None, children=[], state=grid, root=True)
        self.root.UCT = math.inf
        self.first = first
        self.local_grid = grid
        self.symbols = ['X', 'O']
        self.player = player
        self.C = 2**0.5  # Try changing C value
        self.iterate = 1000
        self.count = 0
        self.human = xor(self.player)

    def get_UCT(self, node):
        """For root node: return infinite UCT value
        For other nodes
        if visited: calculate and return UCT value
        if not yet visited: return infinite UCT value
        """
        if self.check_win(node.state) == (0, 1):
            return -math.inf
        elif self.check_win(node.state) == (1, 1):
            return math.inf

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
        """Returns the leaf node with the highest UCT value

           Go through game tree starting from the root node
           Use the children list of each node to find the child with the largest UCT value and select it
           Repeat this until a leaf node is reached
           Return this leaf node

           Are all nodes that have empty children lists leaf nodes?
           Leaf node = one that has no children, has not been expanded to have children.
           Make sure at expansion, the node child is added to its children list"""

        # Dont select nodes with 1 or less child, nodes that have already won should have 0 children
        # for i in self.game_tree:
        #     display_game_tree(self.game_tree, i)

        while len(node.children) > 0:
            for child_node in node.children:
                child_node.UCT = self.get_UCT(child_node)

            children_sorted = sorted(node.children, reverse=True, key=lambda each_node: each_node.UCT)
            node = children_sorted[0]
            equal_UCT_nodes = []

            for sorted_node in children_sorted:
                if sorted_node.UCT == node.UCT:
                    equal_UCT_nodes.append(sorted_node)

            if len(equal_UCT_nodes) > 0:
                node = random.choice(equal_UCT_nodes)
        return node
                # store UCT values with nodes, then sort them by highest.
        # while len(node.children) > 1:
        #     UCT_maximum = 0
        #     UCT_maximiser = None
        #     for child_node in node.children:
        #         child_UCT = self.get_UCT(child_node)
        #         if child_UCT > UCT_maximum:
        #             UCT_maximum = child_UCT
        #             UCT_maximiser = child_node
        #     if UCT_maximiser is not None:
        #         node = UCT_maximiser
        #     else:
        #         node = random.choice(node.children)
        #
        # return node

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
        """Simulate should not create new children, simulate should only be used to back propogate after a random game
        is completed"""
        # turns may not be correct
        node_children = []
        if self.check_win(node.state) is None:
            if player in [1, 0]:
                for x in range(3):  # change this to simulate only in empty spaces
                    for y in range(3):
                        if self.check_move(node.state, (x, y)):
                            new_child = Node(self.game_tree, node, [])
                            new_child.state = [x[:] for x in node.state]
                            new_child.state[y][x] = self.symbols[player]
                            node_children.append(new_child)
                            # print()
                            # print(count % 2)
                            # print(new_child.state)
                            # if self.check_win(new_child.state) == (1, 1):
                            #     return [new_child]
                            # elif self.check_win(new_child.state) != (0, 1) or len(node_children) == 0:
                            #     # need to check for children of the state not for just the state.
                            #     node_children.append(new_child)
        return node_children
                #print(node.children)  # provides good data

    def expand(self, node):
        """Should expand to all child nodes, but only return a random one for simulation"""
        if self.check_win(node.state) is not None:
            return node
        h_move = self.heuristic_move(node)

        if h_move is not None:
            node_children = [h_move]
        else:
            node_children = self.get_children(node, find_turn(node, self.first))

        for child_node in node_children:
            child_node.add_to_game_tree(self.game_tree)
            child_node.parent.children.append(child_node)

        if len(node_children) > 0:
            return random.choice(node_children)
        else:
            return None

    def create_child(self, parent, state):
        child_node = Node(game_tree=self.game_tree, parent=parent, children=[], state=state)
        return child_node

    def heuristic_move(self, node):
        p_num = find_turn(node, self.first)
        p_symb = self.symbols[p_num]
        o_symb = self.symbols[xor(p_num)]
        winners = self.get_winners(node.state)
        template = [[(0, 0), (0, 1), (0, 2)], [(1, 0), (1, 1), (1, 2)], [(2, 0), (2, 1), (2, 2)],
                    [(0, 0), (1, 0), (2, 0)], [(0, 1), (1, 1), (2, 1)], [(0, 2), (1, 2), (2, 2)],
                    [(0, 0), (1, 1), (2, 2)], [(0, 2), (1, 1), (2, 0)]]
        winners_data = []
        for w in range(len(winners)):
            winner = winners[w]
            p_symb_num = winner.count(p_symb)
            o_symb_num = winner.count(o_symb)
            winners_data.append((p_symb_num, o_symb_num))

        # search through and look for a specific number and then search again, needs a seperate search function for
        # searching the dictionary/data structure for specific numbers
        # cant use dictionary since dict cant have same keys, but use a tuple based structure

        if (2, 0) in winners_data:
            winner_num = winners_data.index((2, 0))
            winner = winners[winner_num]
            x, y = template[winner_num][winner.index(' ')]  # w = which winner number it is in winners,
                                                   # shows which trio in template, index' ' gets the index of the empty
            state = [x[:] for x in node.state]
            state[x][y] = p_symb
            return Node(game_tree=self.game_tree, parent=node, children=[], state=state)

        elif (0, 2) in winners_data:
            winner_num = winners_data.index((0, 2))
            winner = winners[winner_num]
            x, y = template[winner_num][winner.index(' ')]

            state = [x[:] for x in node.state]
            state[x][y] = p_symb
            return Node(game_tree=self.game_tree, parent=node, children=[], state=state)


    def simulation(self, selected_node):
        # Introduce new heuristics in simulation,
        # Monte Carlo Tree Search is based on basic heuristics + random simulation
        # + expanding where it seems to be good

        current_node = selected_node
        while self.check_win(current_node.state) is None:
            heuristic_node = self.heuristic_move(current_node)
            if heuristic_node is not None:
                current_node = heuristic_node
            else:
                node_children = self.get_children(current_node, find_turn(current_node, self.first))
                current_node = random.choice(node_children)

        return current_node

        #
        # while self.check_win(current_node.state) is None:
        #     node_children = self.get_children(current_node, find_turn(current_node))
        #
        #     flag = False
        #     for node in node_children:
        #         # if node x's children has a winning node, choose node x.
        #
        #         for node_2 in self.get_children(node, find_turn(selected_node)):
        #             if self.check_win(node_2.state) == (1, 1):
        #                 node_children = self.get_children(node, find_turn(current_node))
        #                 flag = True
        #                 break
        #             elif self.check_win(node_2.state) == (0, 1):
        #
        #                 if node in node_children:
        #                     node_children.remove(node)
        #
        #
        #     if flag is False:
        #         the_twos = {}
        #         for node in node_children:
        #             twos = 0
        #             for win in self.get_winners(node.state):
        #                 if Counter(win)['O'] == 2:
        #                     twos += 1
        #             try:
        #                 the_twos[twos].append(node)
        #             except KeyError:
        #                 the_twos[twos] = [node]
        #
        #         print(the_twos)
        #         abc = sorted(the_twos.items(), reverse=True)
        #         print('abc', abc)
        #         if len(abc) == 3:
        #             return random.choice(abc[2][1:])
        #         elif len(abc) == 2:
        #             print('rand', random.choice(abc[1][1:]))
        #             return random.choice(abc[1][1:])
        #         else:
        #             current_node = random.choice(node_children)
        #
        # return current_node

    def simulate(self, selected_node):
        """ need to edit this and the check_win and turn functions, to make sure they are using the right symbol
        on each iteration of the simulations etc.
        Need to make sure the AI doesnt choose the position which will cause it to lose, and always choses the position
        which will cause it to win in these simulations and in game.
        Make the choices in simulation and game not random, they should be the best for exploitation and
        exploration.

        For each node_children list, check if any node is a win node, if so, use that instead
        check if each node is a loser node, if so, remove it from the random choices unless there are no choices left

        When Human turn in simulation, always select human win and least loss possible,
        When AI turn in simulation always select AI win and least loss possible"""
        win = self.check_win(selected_node.state)

        if win is not None:
            x1, x2 = selected_node.value
            selected_node.value = (x1 + win[0], x2 + win[1])
            self.back_propagate(selected_node, (win[0], 1))
        else:

            current_node = self.simulation(selected_node)

            W1, n1 = selected_node.value
            W2, n2 = self.check_win(current_node.state)  # last edited here...
            selected_node.value = (W1 + W2, n1 + n2)
            self.back_propagate(selected_node, (W2, n2))

        # node_children = self.get_children(selected_node, get_turn(selected_node.state, self.symbols))
        # current_node = selected_node
        # flag = False
        #
        # while len(node_children) > 0 and not flag:
        #
        #     # need to put this section into node_children function
        #     for node in node_children:
        #         if self.check_win(node.state) == (1, 1):
        #             current_node = node
        #             flag = True
        #             break
        #         elif self.check_win(node.state) == (0, 1):
        #             if len(node_children) > 1:
        #                 node_children.remove(node)
        #
        #     if not flag:
        #         current_node = random.choice(node_children)
        #     node_children = self.get_children(current_node, get_turn(current_node.state, self.symbols))

            # till here, check history to see difference, or check sdf.py



        # node_children = self.get_children(selected_node, get_turn(selected_node.state, self.symbols))
        # copy_node = selected_node
        # while len(node_children) > 0:
        #     flag = True
        #     for node in node_children:
        #         if self.check_win(node.state) == (1, 1):
        #             copy_node = node
        #             flag = False
        #     if flag:
        #         copy_node = random.choice(node_children)
        #     self.get_children(copy_node, get_turn(copy_node.state, self.symbols))
        # W1, n1 = selected_node.value
        # W2, n2 = self.check_win(copy_node.state)
        # selected_node.value = (W1 + W2, n1 + n2)

    def back_propagate(self, simulated_node, value):
        W2, n2 = value
        while simulated_node.parent is not None:
            W1, n1 = simulated_node.parent.value
            simulated_node.parent.value = (W1 + W2, n1 + n2)
            simulated_node = simulated_node.parent

    def Monte_Carlo(self):
        for child_node in self.get_children(self.root, 1):
            child_node.parent = self.root
            child_node.parent.children.append(child_node)
            child_node.add_to_game_tree(self.game_tree)

        while self.count <= self.iterate:
            selected_leaf = self.select(self.game_tree[0][0])  # starts selection with root, returns the selected leaf
            # if self.check_win(selected_leaf.state) is not None:
            #     selected_leaf.display_node()
            #     print()

            if selected_leaf.value[1] == 0:  # if node hasn't been visited
                self.simulate(selected_leaf)  # simulate a game from the node and back propagate it
            else:
                simulation_node = self.expand(selected_leaf)
                if simulation_node is not None:
                    self.simulate(simulation_node)
                else:
                    print('1')
            self.count += 1

        move_node = self.make_move()

        return move_node

    def make_move(self):
        """if node is a win, return it, if node's children contain a loss, do not consider it, if theres nothing left,
        choose a random boi"""
        simulation_max = 0
        move_node = None
        a = sorted(self.game_tree[1], reverse=True, key=lambda each_node: each_node.value[1])

        for node in self.game_tree[1]:
            # added this bit again:
            # if self.check_win(node.state) == (1, 1):
            #     return node

            if node.value[1] >= simulation_max:
                simulation_max = node.value[1]
                move_node = node
        heuristic_move = self.heuristic_move(self.game_tree[0][0])
        # if heuristic_move is not None:
        #     move_node = heuristic_move

        return move_node


        # sorted_possibles = sorted(self.game_tree[1], key=lambda node: node.value[1], reverse=True)
        # for node in sorted_possibles:
        #     if self.check_win(node.state) == (1, 1):
        #         return node
        # return sorted_possibles[0]

        # sorted_possibles = sorted(self.game_tree[1], key=lambda node: node.value[1], reverse=True)
        #
        # for node in sorted_possibles:
        #     if self.check_win(node.state) == (1, 1):
        #         return node
        #     for child_node in node.children:
        #         if self.check_win(child_node.state) == (0, 1):
        #             sorted_possibles.remove(node)
        # if len(sorted_possibles) > 0:
        #     return sorted_possibles[0]
        # else:
        #     return random.choice(self.game_tree[1])

    def get_winners(self, grid):
        winners = []
        # right_down = []
        # left_down = []
        # for row in range(len(grid)):
        #     rows = []
        #     columns = []
        #     for column in range(len(rows)):
        #         rows.append(grid[row][column])
        #         columns.append(grid[column][row])
        #         if row == column:
        #             right_down.append(grid[])

        # horizontal
        for x in range(len(grid)):
            row = []
            for y in range(len(grid)):
                row.append(grid[x][y])
            winners.append(row)

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


# Turns is messing something up.
# When AI goes first, AI is good
# When Ai goes second, not as good
# Look at simulation


class Game:
    def __init__(self, game_tree):
        start_state = [[' ', ' ', ' '], # need to add root, not do this
                      [' ', ' ', ' '],
                      [' ', ' ', ' ']]
        self.starting_player_num = 1

        self.turn = self.starting_player_num
        self.mont = MonteCarlo(start_state, game_tree, player=1, first=self.starting_player_num) # used to be player=random.randint(0, 1)
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
                if self.game_node is None:
                    print('ye')
                self.game_node.display_node()

                # for i in range(len(self.mont.game_tree)):
                #     print("Depth:", i)
                #     self.mont.display_game_tree(depth=i)
                #     b = [node for node in self.mont.game_tree[i] if node.value[1] != 0]
                #     print('visited', len(b), 'out of', len(self.mont.game_tree[i]))


                    #self.mont.display_game_tree(self.turn)

            if self.turn == 0:
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
start_time = time.time()
game.run()
print(time.time() - start_time)

# (game.mont.random_move(Node(game.mont.game_tree, None, [], state=[['O', 'O', 'X'],
#                                                                  ['X', 'X', 'O'],
#                                                                  ['O', 'O', 'X']], root=True))).display_node()

# test = [['O', 'O', ' '],
#         [' ', ' ', ' '],
#         [' ', ' ', ' ']]
#
# mont = MonteCarlo(game_tree={0: []}, grid=test)
#
# print(mont.simulate(Node(state=test, parent=[], children=[], root=True, game_tree=mont.game_tree)))

# sort out turns in get_children


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


# what about child nodes that have won?


# Make sure in simulation and game, when the winning (/losing aswell for simulation)
# move is available, it is always chosen.


# How to store node relations?
# Game Tree, contains all nodes according to their depth
# Parent/Children in nodes
# Use parent/child instead of game_tree
# Make sure the 1st Depth are added most early
# Instead of depth searching, search through all until the correct number of the 1st depth is reached
# Then select the most visited node from here
# Need to make a tree structure instead with parents and depths and all stored in one structure
