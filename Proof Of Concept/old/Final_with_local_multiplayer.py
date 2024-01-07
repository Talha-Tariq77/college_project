import math
import random

winners = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8),
           (0, 4, 8), (2, 4, 6)]
symbols = ['X', 'O']

default_starting_state = ['         ', '         ', '         ', '         ', '         ',
                          '         ', '         ', '         ', '         ']

def input_convertor(coordinate, reverse=False):
    # Parameters :- coordinate:string, reverse:boolean
    # Return Type :- tuple
    # Purpose :- Converts string 2 digit coordinate into keypad tuple or vice versa
    ###########################

    conv = [7, 8, 9, 4, 5, 6, 1, 2, 3]
    x, y = int(coordinate[0]), int(coordinate[1])

    if not reverse:
        acc_coordinate = (conv.index(x), conv.index(y))
    else:
        acc_coordinate = (conv[x], conv[y])
    return acc_coordinate


def opposite(dig):
    # Parameters :- dig:integer (1 or 0)
    # Return Type :- integer
    # Purpose :- Returns 1 for 0 and vice versa
    ###########################

    if dig == 1:
        return 0
    else:
        return 1


def check_move(grid, coordinate):
    # Parameters :- grid: list, coordinate: tuple
    # Return Type :- boolean
    # Purpose :- Checks whether or not a move is valid
    a, b = coordinate
    if len(grid[a]) <= 1:
        return False

    if grid[a][b] != ' ':
        return False

    return True


def get_valid_moves(node_state, prev_move):
    # Parameters :- node_state:list, prev_move:tuple
    # Return Type :- list
    # Purpose :- Returns a list of all valid child states of a node state
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


def check_win(global_grid):
    # Parameters :- global_grid: list
    # Return Type :- tuple
    # Purpose :- Checks and returns whether the game state has been won, lost or drawn
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
        else:
            self.current_player = opposite(self.parent.current_player)
            self.depth = self.parent.depth + 1

    def display_node(self):
        # Parameters :- None
        # Return Type :- None
        # Purpose :- Prints the Node.state in a clear format
        state_copy = self.state[:]
        for grid in range(len(state_copy)):
            if state_copy[grid] == 'O':
                state_copy[grid] = 'OOOOOOOOO'
            elif state_copy[grid] == 'X':
                state_copy[grid] = 'XXXXXXXXX'

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
        print()


class MonteCarlo:
    def __init__(self, grid, prev_move=None):
        self.root = Node(parent=None, children=[], state=grid, root=True, prev_move=prev_move)
        self.C = 2 ** 0.5
        self.iterate = 1000
        self.count = 0

    def get_UCT(self, node):
        # Parameters :- node:Node
        # Return Type :- float
        # Purpose :- Calculates a UCT value for a Node and returns it
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
        # Parameters :- node:Node
        # Return Type :- Node
        # Purpose :- Finds the leaf Node and the pathway to it which maximises the UCT equation
        while len(node.possible_moves) == 0:
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
        # Parameters :- node:Node
        # Return Type :- Node
        # Purpose :- creates and returns a random child node of the node
        expansion_move = random.choice(node.possible_moves)
        new_child_node = self.create_child_node(parent=node, move=expansion_move)

        return new_child_node

    def simulation(self, selected_node):
        # Parameters :- selected_node:Node
        # Return Type :- tuple
        # Purpose :- Simulates a random game from selected_node and returns the terminal state: (W, L, D)
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
        # Parameters :- selected_node:Node
        # Return Type :- None
        # Purpose :- adds the correct values to the correct Nodes, calls the simulation and back_propagate methods
        sim_result = self.simulation(selected_node)

        W1, n1 = selected_node.value
        W2, n2 = sim_result
        selected_node.value = (W1 + W2, n1 + n2)
        self.back_propagate(selected_node, (W2, n2))

    def back_propagate(self, simulated_node, value):
        # Parameters :- simulate_node: Node, value:tuple
        # Return Type :- None
        # Purpose :- adds value to the Node.value of each parent of the simulated_node until root is reached
        W2, n2 = value
        while simulated_node.parent is not None:
            W1, n1 = simulated_node.parent.value
            simulated_node.parent.value = (W1 + W2, n1 + n2)
            simulated_node = simulated_node.parent

    def Monte_Carlo(self):
        # Parameters :- None
        # Return Type :- Node
        # Purpose :- Executes the MCTS algorithm and calls the make_move, returns the best move
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
        # Parameters :- None
        # Return Type :- Node
        # Purpose :- Finds best move Node, returns it
        max_visits = 0
        move_node = None

        for node in self.root.children:
            if node.value[1] >= max_visits:
                max_visits = node.value[1]
                move_node = node

        return move_node

    def create_child_node(self, parent, move):
        # Parameters :- parent:Node, move:tuple
        # Return Type :- Node
        # Purpose :- Creates child_node such that parent+move=child_node
        child_node = Node(parent, [], prev_move=move, state=parent.state[:])

        a, b = move
        child_node.state[a] = child_node.state[a][:b] + symbols[parent.current_player] \
                              + child_node.state[a][b + 1:]

        parent.possible_moves.remove(move)
        child_node.parent.children.append(child_node)
        return child_node


class Game:
    def __init__(self, mode, starting_state=None, prev_move=None, starting_player_num=random.choice([0, 1])):
        # starting_player_num decides if the human(0) or AI(1) goes first
        if starting_state is None:
            starting_state = ['         ', '         ', '         ', '         ', '         ',
                              '         ', '         ', '         ', '         ']
        self.starting_player_num = starting_player_num
        self.turn = self.starting_player_num
        self.prev_move = prev_move

        self.mode = mode
        self.players = [['Player 1', 'Player 2'], ['Human Player', 'AI']][self.mode]
        self.mont = MonteCarlo(grid=starting_state,
                               prev_move=self.prev_move)
        self.result = None
        self.game_node = self.mont.root
        self.turn_count = 0

    def AI_turn(self):
        print("AI Turn")
        if self.game_node.state == default_starting_state:
            self.game_node = self.mont.create_child_node(self.mont.root, (4, 4))
            self.prev_move = (4, 4)
        else:
            self.game_node = self.mont.Monte_Carlo()

            self.prev_move = self.game_node.prev_move

    def player_turn(self):
        print(self.players[self.turn])
        player_move = input('Coordinates: ')
        if player_move == '000':
            print('Game state saved and game aborted')
            quit()

        while self.handle_input(player_move) is False:
            print("Invalid Move!")
            player_move = input('Coordinates: ')
            if player_move == '000':
                print('Game Aborted')
                quit()

        a, b = input_convertor(player_move, reverse=False)

        self.game_node.state[a] = self.game_node.state[a][:b] + symbols[self.turn] + self.game_node.state[a][b + 1:]
        self.prev_move = (a, b)
        self.game_node.prev_move = self.prev_move

    def run(self):
        # Parameters :- None
        # Return Type :- None
        # Purpose :- Returns the Ultimate Tic Tac Toe Game
        self.game_node.display_node()
        if self.prev_move is not None:
            print('previous:', input_convertor(self.prev_move, reverse=True))

        while self.result is None:
            if self.turn_count > 0:
                self.save_game(self.game_node.state, self.turn, self.prev_move)

            if self.turn == 1 and self.mode == 1:
                self.AI_turn()
            elif self.turn == 1 and self.mode == 0:
                self.player_turn()

            if self.turn == 0:
                self.player_turn()

            self.turn_count += 1

            self.result = check_win(self.game_node.state)

            self.game_node.display_node()

            print('previous:', input_convertor(self.prev_move, reverse=True))

            if self.mode == 1:
                self.mont.__init__(self.game_node.state, prev_move=self.prev_move)

            self.turn = opposite(self.turn)
        self.endgame()
        self.clear_save()

    def handle_input(self, coordinate):
        # Parameters :- coordinate:tuple
        # Return Type :- Boolean
        # Purpose :- check if the input coordinate is valid or not
        if len(coordinate) != 2:
            return False

        for val in coordinate:
            if val not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                return False

        a, b = input_convertor(coordinate)

        move_check = check_move(self.mont.root.state, (a, b))
        if move_check is False:
            return move_check

        if self.prev_move is not None:
            if not len(self.game_node.state[self.game_node.prev_move[1]]) == 1 \
                    and not a == self.game_node.prev_move[1]:
                return False

    def endgame(self):
        # Parameters :- None
        # Return Type :- None
        # Purpose :- Displays a Win/Loss/Draw string at end of game
        if self.result == (1, 1):
            print(self.players[1] + ' won!')
        elif self.result == (0, 1):
            print(self.players[0] + ' won!')
        else:
            print("Draw!")

    def save_game(self, game_state, turn, prev_move):
        save_file = open('save_file.txt', 'w')
        for local_grid in game_state:
            save_file.write(local_grid + '\n')
        save_file.write(str(turn) + '\n')
        save_file.write(str(prev_move[0]) + str(prev_move[1]))
        save_file.close()

    def clear_save(self):
        open('save_file.txt', 'w').close()


'''Save works when both AI and human turn and in all cases as it should, I believe
Could have inheritance for human vs human and human vs AI different game modes
work on
navigation
instructions
starting player changes
Then testing- difficulty
testing etc.'''


class Menu:
    def __init__(self):
        self.main_menu = ['New Game', 'Load Game', 'Exit']
        self.current_menu = self.main_menu
        self.menu_option = None

    def display(self):
        for i in range(len(self.current_menu)):
            print(i + 1, '-', self.current_menu[i])

    def user_choose(self):
        option = input(': ')

        while option not in [str(x) for x in range(1, len(self.current_menu) + 1)]:
            print('Invalid')
            return input(': ')

    def new_game(self):
        settings = ''
        for menu in [['Local Multiplayer', 'Human vs AI'], ['Easy', 'Medium', 'Hard']]:
            self.current_menu = menu
            self.display()
            settings += self.user_choose()

        game = Game(settings[0])
        game.run()

    def load_game(self):
        last_save = open('save_file.txt', 'r')
        data = last_save.readlines()
        save_state = [x[:-1] for x in data[:-2]]
        print(data)
        save_player_num = int(data[-2])
        save_prev_move = (int(data[-1][0]), int(data[-1][1]))

        game = Game(save_state, save_prev_move, save_player_num)
        last_save.close()
        game.run()

    def run(self):
        self.display()
        self.menu_option = self.user_choose()

        if self.menu_option == '1':
            self.new_game()
        elif self.menu_option == '2':
            self.load_game()
        else:
            quit()


menu = Menu()
menu.run()
