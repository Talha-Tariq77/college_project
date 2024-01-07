import math
import random
# from copy import deepcopy
import time

how_much_to_expand = 1  # works 2000000 times better than lesser expansion rates
winners = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8),
                   (0, 4, 8), (2, 4, 6)]
symbols = ['X', 'O']

start_state = ['         ', '         ', '         ', '         ', '         ',
               '         ', '         ', '         ', '         ']

# fix gameplay
# test different node expansions
# try using RAVE and 'domain specific expert knowledge'
# maybe put in some threading


def input_convertor(coordinate, reverse=False):
    """Coordinate: string"""
    conv = [7, 8, 9, 4, 5, 6, 1, 2, 3]
    x, y = int(coordinate[0]), int(coordinate[1])

    if not reverse:
        acc_coordinate = (conv.index(x), conv.index(y))
    else:
        acc_coordinate = (conv[x], conv[y])
    return acc_coordinate


def opposite(dig):
    if dig == 1:
        return 0
    else:
        return 1


def check_move(grid, coordinate):

    a, b = coordinate
    if len(grid[a]) <= 1:
        return False

    if grid[a][b] != ' ':
        return False

    return True


def get_valid_moves(node_state, prev_move):
    valid_moves = []
    if prev_move is None:
        for a in range(9):
            for b in range(9):
                valid_moves.append((a, b))

    else:
        x, y = prev_move
        if ' ' not in node_state[y]:
            for a in range(9):
                for b in range(9):
                    if check_move(node_state, (a, b)):
                        valid_moves.append((a, b))
        else:
            for a in range(9):
                if check_move(node_state, (y, a)):
                    valid_moves.append((y, a))

    return valid_moves


    # def start(self):
    #     print("""Ultimate Tic Tac Toe\nStart-Enter\nInstructions-I\nQuit-Q""")
    #     choice = input(': ').lower()
    #     while choice not in ['\n', 'i', 'q']:
    #         choice = input()

def check_win(global_grid):
    for i in range(len(global_grid)):
        current_grid = global_grid[i]
        if len(current_grid) > 1:
            for winner in winners:
                a, b, c = winner
                grid_winner = current_grid[a] + current_grid[b] + current_grid[c]
                if grid_winner == 'XXX':
                    global_grid[i] = 'X'
                    break
                elif grid_winner == 'OOO':
                    global_grid[i] = 'O'
                    break
    # can I find a better way to do this than by finding all local grids and replacing by singles.

    for winner in winners:
        a, b, c = winner
        global_winner = global_grid[a] + global_grid[b] + global_grid[c]
        if global_winner == 'OOO':
            return 1, 1
        elif global_winner == 'XXX':
            return 0, 1

    for grid in global_grid:
        if ' ' in grid:
            return None
    return 0.5, 1


game_tree = {0: []}


class Node:
    def __init__(self, parent, children, prev_move, state=None, root=False, value=(0, 0)):
        self.parent = parent
        self.children = children
        self.value = value  # q/Q = wins/ vists
        self.state = state
        self.root = root
        self.UCT = None
        self.prev_move = prev_move
        self.possible_moves = get_valid_moves(node_state=self.state, prev_move=self.prev_move)

        if root:
            self.current_player = 1  # this makes it so that the AI player is O
            self.depth = 0
            if len(game_tree[self.depth]) > 0:
                game_tree[self.depth][0] = self
            else:
                game_tree[self.depth].append(self)
        else:
            self.current_player = opposite(self.parent.current_player)
            # current player is the players symbol that will be applied to its children
            self.depth = self.parent.depth + 1
            self.add_to_game_tree()

    def add_to_game_tree(self):
        if not len(game_tree) > self.depth:
            game_tree[self.depth] = []

        game_tree[self.depth].append(self)

    def __repr__(self):
        # return str(self.value)
        # return '{}, {}, {} UCT: {}, val: {}'.format(self.state[0], self.state[1], self.state[2], self.UCT, self.value)
        return 'UCT: {}, val: {}'.format(self.UCT, self.value)

    def display_node(self):
        ''' for first 3 grids, print first 3,
        for'''
        state_copy = self.state[:]
        for grid in range(len(state_copy)):
            if state_copy[grid] == 'O':
                state_copy[grid] = 'OOOOOOOOO'
            elif state_copy[grid] == 'X':
                state_copy[grid] = 'XXXXXXXXX'
        # print('acc state', self.state)

        print('╔' + '═' * 18 + '╗')
        for z in range(3):
            for i in range(3):
                for grid in state_copy[z * 3:(z + 1) * 3]:
                    print('║' + grid[i * 3:(i + 1) * 3].replace(' ', '☐'), end='║')
                print()
            if z == 2:
                print('╚' + '═' * 18 + '╝')
            else:
                print('╠' + '═' * 18 + '╣')
        # for i in range(3):
        #     for grid_num in range(3):
        #         for grids in self.state[grid_num * 3: (grid_num + 1) * 3]:
        #             for grid in grids:
        #                 for char_num in range(i * 3, (i + 1) * 3):
        #                     if grid[char_num] == ' ':
        #                         print('☐', end='')
        #                     else:
        #                         print(grid[char_num], end='')
        print()

        # print('-' * 20)
        # for global_row_num in range(3):
        #     for row in range(3):
        #         for lcl_board_num in range(3):
        #             print('|', end='')
        #             # print(global_row_num, lcl_board_num, row)
        #             for symb in self.state[global_row_num][lcl_board_num][row]:
        #                 if symb == ' ':
        #                     print('☐', end='')
        #                 else:
        #                     print(symb, end='')
        #             print('|', end='')
        #         print()
        #     print('-'*20)

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
    def __init__(self, grid, prev_move=None):
        self.game_tree = game_tree  # temporary, for debugging
        self.root = Node(parent=None, children=[], state=grid, root=True, prev_move=prev_move)
        # print('possibles', self.root.possible_moves)
        # self.root.UCT = math.inf
        self.C = 2 ** 0.5  # Try changing C value
        self.iterate = 10000
        self.count = 0
        # self.start_time = time.time()
        # self.end_time = time.time() + 5

    def get_UCT(self, node):
        if node.parent:
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

        # while len(node.possible_moves) > 0 and len(node.children) > 0:  # check this stop when no possible moves,
                                                                        # or when no children to expand
        while len(node.possible_moves) == 0:
#  if node is not fully expanded, stop and select that node
            # Not properly checking if child nodes are left.
            for child_node in node.children:
                child_node.UCT = self.get_UCT(child_node)

            children_sorted = sorted(node.children, reverse=True, key=lambda each_node: each_node.UCT)
            node = children_sorted[0]

            # Randomise equal nodes:
            equal_UCT_nodes = []

            for sorted_node in children_sorted:
                if sorted_node.UCT == node.UCT:
                    equal_UCT_nodes.append(sorted_node)

            if len(equal_UCT_nodes) > 0:
                node = random.choice(equal_UCT_nodes)
        return node

    def expand(self, node):
        """Should expand to all child nodes, but only return a random one for simulation"""
        # if self.check_win(node.state) is not None:
        #     return node

        expansion_move = random.choice(node.possible_moves)
        new_child_node = self.create_child_node(parent=node, move=expansion_move)

        return new_child_node

        # if len(node_children) > 0:
        #     return random.choice(node_children)
        # else:
        #     return None

    def simulation(self, selected_node):
        current_player = selected_node.current_player
        current_state = selected_node.state[:]
        prev_move = selected_node.prev_move

        is_terminal = check_win(current_state)

        while is_terminal is None:
            possible_moves = get_valid_moves(current_state, prev_move)

            random_move = random.choice(possible_moves)

            ra, rb = random_move
            current_state[ra] = current_state[ra][:rb] + symbols[current_player] \
                                + current_state[ra][rb + 1:]
            is_terminal = check_win(current_state)
            prev_move = random_move
            current_player = opposite(current_player)

        return is_terminal

    def simulate(self, selected_node):
        sim_result = self.simulation(selected_node)

        W1, n1 = selected_node.value
        W2, n2 = sim_result
        selected_node.value = (W1 + W2, n1 + n2)
        self.back_propagate(selected_node, (W2, n2))

    def back_propagate(self, simulated_node, value):
        W2, n2 = value
        while simulated_node.parent is not None:
            W1, n1 = simulated_node.parent.value
            simulated_node.parent.value = (W1 + W2, n1 + n2)
            simulated_node = simulated_node.parent

    def Monte_Carlo(self):
        while self.count <= self.iterate:
            # select the node with the highest UCT value
            selected_leaf = self.select(self.root)

            # if Node hasn't been visited
            if selected_leaf.value[1] == 0:
                # simulate a game from the Node and back propagate it
                self.simulate(selected_leaf)

            else:  # if Node has been visited
                # expand the Node
                simulation_node = self.expand(selected_leaf)

                # and simulate the new Child Node
                self.simulate(simulation_node)

            self.count += 1

        # AI move is the immediate child node
        # of the root that has been visited most
        move_node = self.make_move()

        return move_node

    def make_move(self):
        max_visits = 0
        move_node = None

        for node in self.root.children:
            if node.value[1] >= max_visits:
                max_visits = node.value[1]
                move_node = node

        return move_node

    def create_child_node(self, parent, move):
        child_node = Node(parent, [], prev_move=move, state=parent.state[:])

        a, b = move
        child_node.state[a] = child_node.state[a][:b] + symbols[parent.current_player] \
                              + child_node.state[a][b + 1:]

        parent.possible_moves.remove(move)
        child_node.parent.children.append(child_node)
        return child_node

    def heuristic_prune(self, state, possible_moves, current_player):
        # print(node.state)
        corners = [0, 2, 6, 8]
        move_values = {}
        for move in possible_moves:
            a, b = move
            current_state = state[:]
            current_state[a] = current_state[a][:b] + symbols[current_player] \
                                + current_state[a][b + 1:]
            res = check_win(current_state)
            score = 0

            if current_state[4] == symbols[current_player]:
               score += 10
            elif current_state[4] == symbols[opposite(current_player)]:
                score -= 10

            for i in corners:
                if current_state[i] == symbols[current_player]:
                    score += 5
                elif current_state[i] == symbols[opposite(current_player)]:
                    score += 5

            if score >= 0 or len(move_values) < 1:
                move_values[move] = score
            pass


class Game:
    def __init__(self):
        self.starting_player_num = 1  # decides if the human(0) or AI(1) goes first

        self.turn = self.starting_player_num
        self.prev_move = None

        self.mont = MonteCarlo(grid=start_state,
                               prev_move=self.prev_move)
        self.result = None
        self.game_node = self.mont.root
        self.turn_count = 0

    def run(self):
        self.game_node.display_node()
        while self.result is None:

            if self.turn == 1:
                print("AI Turn")
                if self.turn_count == 0:
                    self.game_node = self.mont.create_child_node(self.mont.root, (4, 4))
                    self.prev_move = (4, 4)
                else:
                    self.game_node = self.mont.Monte_Carlo()

                    self.prev_move = self.game_node.prev_move

            if self.turn == 0:
                print("Human Turn")
                human_move = input('Coordinates: ')
                if human_move == '000':
                    print('Game Aborted')
                    quit()

                while self.handle_input(human_move) is False:
                    print("Invalid Move!")
                    human_move = input('Coordinates: ')
                    if human_move == '000':
                        print('Game Aborted')
                        quit()

                a, b = input_convertor(human_move, reverse=False)

                self.game_node.state[a] = self.game_node.state[a][:b] + 'X' + self.game_node.state[a][b + 1:]
                self.prev_move = (a, b)

            self.turn_count += 1

            self.result = check_win(self.game_node.state)

            self.game_node.display_node()

            print(input_convertor(self.prev_move, reverse=True))

            self.mont.__init__(self.game_node.state, prev_move=self.prev_move)

            self.turn = opposite(self.turn)
        self.endgame()

    def handle_input(self, coordinate):
        if len(coordinate) != 2:
            return False

        for val in coordinate:
            if val not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                return False

        a, b = input_convertor(coordinate)

        move_check = check_move(self.mont.root.state, (a, b))
        if move_check is False:
            return move_check

        if not len(self.game_node.state[self.game_node.prev_move[1]]) == 1 \
                and not a == self.game_node.prev_move[1]:
            return False

    def endgame(self):
        if self.result == (1, 1):
            print("Computer Won!")
        elif self.result == (0, 1):
            print("Human Won!")
        else:
            print("Draw!")

    # def record(self):
    #     file = open('record.txt', 'a')
    #     file.write(str(self.result[0]) + '\n')
    #     file.close()

# game = Game()
# game.run()

if __name__ == '__main__':
    import cProfile

    get_valid_moves(start_state, prev_move=(4,4))
    p = cProfile.Profile()
    p.enable()
    # game = Game()
    # game.run()
    mont = MonteCarlo(grid=start_state, prev_move=(4, 4))
    mont.root.state[4] = '    X    '
    mont.root.display_node()
    chosen_node = check_win(mont.root.state)
    print(chosen_node)
    # chosen_node = mont.Monte_Carlo()
    # chosen_node.display_node()

    # Go through each part of the monte_carlo function one by one
    # Put breakpoints on each part and see

    p.disable()

    p.print_stats(sort='tottime')
