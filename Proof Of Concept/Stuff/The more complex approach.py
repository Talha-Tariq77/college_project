import math
import random
from copy import deepcopy
import time

def tuple_conv(tup):
    """Input: Tuple, Output: Printable string of tuple"""
    x, y = tup
    if x == 0.5:
        x = 5
    return str(x) + ' ' + str(y)

def seperate(alist):
    new_list = []
    for i in range(len(alist)):
        if i % 3 == 0:
            seperations = [a[:] for a in alist[i:i+3]]
            new_list.append(seperations)
    return new_list


def find_turn(node_state, first):
    x = 0
    o = 0
    for grid in node_state:
        for i in range(len(grid)):
            if grid[i] == 'X':
                x += 1
            elif grid[i] == 'O':
                o += 1
    if x == o:
        return first
    elif x > o:
        return 1
    else:
        return 0


def display_game_tree(game_tree, x):
    print()
    level = game_tree[x]
    for node in level:
        node.display_node()
        print(node)


def input_convertor(coordinate):
    """Coordinate: string"""

    acc_coordinate = []
    for number in coordinate:
        number = int(number)
        x, y = None, None
        conv = [[7, 8, 9], [4, 5, 6], [1, 2, 3]]
        for row in conv:
            if number in row:
                x = conv.index(row)
                y = row.index(number)
                acc_coordinate.append(x)
                acc_coordinate.append(y)
    return acc_coordinate


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
        self.possible_children = []

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
        #return '{}, {}, {} UCT: {}, val: {}'.format(self.state[0], self.state[1], self.state[2], self.UCT, self.value)
        return 'UCT: {}, val: {}'.format(self.UCT, self.value)

    def display_node(self):
        print('-' * 20)
        for global_row_num in range(3):
            for row in range(3):
                for lcl_board_num in range(3):
                    print('|', end='')
                    # print(global_row_num, lcl_board_num, row)
                    for symb in self.state[global_row_num][lcl_board_num][row]:
                        if symb == ' ':
                            print('☐', end='')
                        else:
                            print(symb, end='')
                    print('|', end='')
                print()
            print('-'*20)

        # for row in self.state:
        #     for pos in row:
        #         if pos == ' ':
        #             print('☐', end='')
        #         else:
        #             print(pos, end='')
        #     print()

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
        self.called = 0
        self.C = 2**0.5  # Try changing C value
        self.iterate = 100
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

        # while len(node.children) > 0:
        while len(node.possible_children) == 0:
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

    def check_move(self, grid, coordinate):
        # coordinate list or tuple of len 4
        a, b = coordinate

        if grid[a][b] != ' ':
            return False

        return True

    def get_children(self, node, player):
        self.called += 1
        """Simulate should not create new children, simulate should only be used to back propogate after a random game
        is completed"""
        # turns may not be correct
        node_children = []
        if self.check_win(node.state) is None:
            for a in range(9):
                for b in range(9):
                    if self.check_move(node.state, (a, b)):
                        new_child = Node(self.game_tree, node, [])

                        new_child.state = node.state[:]
                        new_child.state[a] = new_child.state[a][:b] + self.symbols[player] + new_child.state[a][b+1:]
                        node_children.append(new_child)

        return node_children

    def expand(self, node):
        """Should expand to all child nodes, but only return a random one for simulation"""
        if self.check_win(node.state) is not None:
            return node

        # node_children = self.get_children(node, find_turn(node.state, self.first))
        # node.possible_children = node_children

        expansion_node = random.choice(node.possible_children)
        expansion_node.parent.children.append(expansion_node)
        expansion_node.add_to_game_tree(self.game_tree)
        node.possible_children.remove(expansion_node)

        # for child_node in node_children:
        #     child_node.add_to_game_tree(self.game_tree)
        #     child_node.parent.children.append(child_node)

        # if len(node_children) > 0:
        #     return random.choice(node_children)
        # else:
        #     return None

        return expansion_node

    def simulation(self, selected_node):
        current_state = selected_node.state[:]

        while self.check_win(current_state) is None:
            random_move = (random.randint(0, 8), random.randint(0, 8))
            while not self.check_move(current_state, random_move):
                random_move = (random.randint(0, 8), random.randint(0, 8))
            ra, rb = random_move
            current_state[ra] = current_state[ra][:rb] + self.symbols[find_turn(current_state, self.first)]\
                                + current_state[ra][rb + 1:]

            # node_children = self.get_children(current_node, find_turn(current_node, self.first))
            # current_node = random.choice(node_children)

        return current_state

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

            current_state = self.simulation(selected_node) # This and selection takes longest amount of time.
            # Try changing code
            # Try using the other method of storage.

            W1, n1 = selected_node.value
            W2, n2 = self.check_win(current_state)  # last edited here...
            selected_node.value = (W1 + W2, n1 + n2)
            self.back_propagate(selected_node, (W2, n2))

    def back_propagate(self, simulated_node, value):
        W2, n2 = value
        while simulated_node.parent is not None:
            W1, n1 = simulated_node.parent.value
            simulated_node.parent.value = (W1 + W2, n1 + n2)
            simulated_node = simulated_node.parent

    def Monte_Carlo(self):
        while len(self.root.possible_children) != 0:
            self.expand(self.root)
        # for child_node in self.get_children(self.root, 1):
        #     child_node.parent = self.root
        #     child_node.parent.children.append(child_node)
        #     child_node.add_to_game_tree(self.game_tree)

        while self.count <= self.iterate:
            selected_leaf = self.select(self.game_tree[0][0])  # starts selection with root, returns the selected leaf

            if selected_leaf.value[1] == 0:  # if node hasn't been visited
                self.simulate(selected_leaf)  # simulate a game from the node and back propagate it
            else:
                simulation_node = self.expand(selected_leaf)
                if simulation_node is not None:
                    self.simulate(simulation_node)
                else:
                    print('1')
            print(self.count)
            if self.count >= 80:
                print('hi')
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

        return move_node

    def get_winners(self, grid):
        winners = []

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

    def check_win(self, global_grid):
        winners = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8),
                   (0, 4, 8), (2, 4, 6)]
        for i in range(len(global_grid)):
            for winner in winners:
                a, b, c = winner
                grid_winner = global_grid[i][a] + global_grid[i][b] + global_grid[i][c]
                if grid_winner == 'XXX':
                    global_grid[i] = 'L' * 9
                elif grid_winner == 'OOO':
                    global_grid[i] = 'W' * 9

            if ' ' not in global_grid[i] and 'W' not in global_grid[i] \
                    and 'L' not in global_grid[i] and 'D' not in global_grid[i]:
                global_grid[i] = 'D' * 9

        global_win = '         '
        for i in range(len(global_grid)):
            for asymb in ['W', 'L', 'D']:
                if asymb in global_grid[i]:
                    global_win = global_win[:i] + asymb + global_win[i+1:]
                    a = len(global_win)

        for i in range(len(global_win)):
            for winner in winners:
                a, b, c = winner
                global_winner = global_win[a] + global_win[b] + global_win[c]
                if global_winner == 'WWW':
                    return 1, 1
                elif global_winner == 'LLL':
                    return 0, 1

        if ' ' not in global_win:
            return 0.5, 1



class Game:
    def __init__(self, game_tree):
        start_state = ['         ',
                       '         ',
                       '         ',
                       '         ',
                       '         ',
                       '         ',
                       '         ',
                       '         ',
                       '         ']
        # start_state = [[[[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']],
        #                [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']],
        #                [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]],
        #
        #                [[[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']],
        #                 [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']],
        #                 [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]],
        #
        #                [[[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']],
        #                 [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']],
        #                 [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]]]

        self.starting_player_num = 1

        self.turn = self.starting_player_num
        self.mont = MonteCarlo(start_state, game_tree, player=1, first=self.starting_player_num) # used to be player=random.randint(0, 1)
        self.result = None
        self.wins = (0, 0)  # comp, h
        self.game_node = self.mont.root

    def run(self):
        while self.result is None:
            print('turn', self.turn)
            print(self.mont.root.state)

            if self.turn == 1:
                print("Computer Turn")
                start_time = time.time()
                self.game_node = self.mont.Monte_Carlo()
                print(time.time() - start_time)
                if self.game_node is None:
                    print('Game node is none')
                print(self.game_node)

            if self.turn == 0:
                print("Human Turn")
                human_move = input('Coordinates: ')
                a, b = int(human_move[0]), int(human_move[1])

                self.game_node.state[a] = self.game_node.state[a][:b] + 'X' + self.game_node.state[a][b+1:]

            self.mont.__init__(self.game_node.state, {0: []})

            self.result = self.mont.check_win(self.game_node.state)

            self.turn = xor(self.turn)
        self.mont.root.display_node()
        self.endgame()

    def handle_input(self, coordinate):
        if len(coordinate) != 2:
            return False

        for val in coordinate:
            if val not in [str(y) for y in list(range(10))]:
                return False

        a, b, c, d = input_convertor(coordinate)
        move_check = self.mont.check_move(self.mont.root.state, (a, b, c, d))
        return move_check
        #
        # if self.game_node.state[a][b][c][d] != ' ':
        #     return False
        # return True

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


game = Game({0: []})
game.run()
# start_time = time.time()
# print(time.time() - start_time)
print(game.mont.called)

# global_grid = ['         ',
#                '         ',
#                '         ',
#                '         ',
#                '         ',
#                '         ',
#                '         ',
#                '         ',
#                '         ']
