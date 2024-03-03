from Node import Node
import random
import math
import Globals
import pickle

import copy

class MonteCarlo:
    def __init__(self, prev_move, init_state, init_major_grid, possible_moves, player) -> None:
        self.prev_move = prev_move[:]

        self.init_state = init_state
        self.init_major_grid = init_major_grid
        self.init_possible_moves = possible_moves
        self.init_player = player
        self.init_prev_move = prev_move

        self.current_state = copy.deepcopy(init_state)
        self.major_grid = init_major_grid[:]
        self.possible_moves = copy.deepcopy(possible_moves)
        self.player = player

        self.C = math.log(2)

        self.root = Node(self.prev_move)

        self.generate_root_children()

        self.current_node = self.root

        self.select_order = []
        self.all_children_selections = []

        self.exploitation_vs_exploration = [0, 0]
        self.all_UTC_values = []

        self.depth = -1
        self.all_node_data = []

        # allows me to monitor which part of the equation is supposedly having the biggest impact
        # on selection at any given time
    
    def generate_root_children(self):
        if self.prev_move == (-1,-1) or not self.possible_moves[self.prev_move[1]]:
            for x in range(len(self.possible_moves)):
                for y in self.possible_moves[x]:
                    self.root.children.append(Node((x,y), self.root))
        else:
            for x in self.possible_moves[self.prev_move[1]]:
                self.root.children.append(Node((self.root.prev_move[1], x), self.root))
        
        # i need to initialise the first child nodes with the UTC value
        # whenever I generate a child node, i need to calculate its UTC
        # otherwise UTC is only updated by selecting a node then backpropogating it
        # it wont update its siblings.
            
    def UTC_calculate(self, a):
        if a.win == a.sim == 0:
            exploitation = 0
        else:
            exploitation = a.win / a.sim
        if a.parent.sim == 0:
            exploration = 0
        elif a.sim == 0:
            exploration = 3
        else:
            exploration = self.C * (math.sqrt(math.log(a.parent.sim) / a.sim))
        self.exploitation_vs_exploration[0] += exploitation
        self.exploitation_vs_exploration[1] += exploration
        return exploitation + exploration
        

    def find_best_UTC(self, nodes):
        best_nodes = [nodes[0]]

        for node in nodes[1:]:
            if node.UTC == best_nodes[0].UTC:
                best_nodes.append(node)

            elif node.UTC > best_nodes[0].UTC:
                best_nodes = [node]
        
        return best_nodes
    
    def selection(self):
        """ if current state has no children:
        return the state
        if it has children, current=child which maximises UTC formula
        update current_state, and possible moves to confirm the selection

        root starts as having all its children expanded. """

        this_selection = []
        
        
        # find best utc should minimise if player 0, maximise if player 1 or whatever it is, not just always minimise
        while self.current_node.children:
            if self.depth == 0:
                # current_UTCs = [((x.win / x.sim), self.C * (math.sqrt(math.log(x.parent.sim) / x.sim)), x.UTC) for x in self.current_node.children]
                pass
            self.depth += 1
            for child in self.current_node.children:
                child.UTC = self.UTC_calculate(child)
            self.current_node = random.choice(self.find_best_UTC(self.current_node.children))

            if self.depth < len(self.all_children_selections):
                if self.current_node.prev_move in self.all_children_selections[self.depth].keys():
                    self.all_children_selections[self.depth][self.current_node.prev_move] += 1
                else:
                    self.all_children_selections[self.depth][self.current_node.prev_move] = 1
            else:
                self.all_children_selections.append({self.current_node.prev_move: 1})
            #     self.all_children_selections[self.depth].append(self.current_node.prev_move)
            # else:
            #     self.all_children_selections[self.depth] = [self.current_node.prev_move]

            if self.current_node.prev_move[1] not in self.possible_moves[self.current_node.prev_move[0]]:
                pass
            self.possible_moves[self.current_node.prev_move[0]].remove(self.current_node.prev_move[1])

            self.current_state[self.current_node.prev_move[0]][self.current_node.prev_move[1]] = Globals.winners[self.player]

            Globals.updateMajorGrid(self.major_grid, self.current_state, self.current_node.prev_move, self.possible_moves)

            self.prev_move = self.current_node.prev_move

            self.player = Globals.swap(self.player)

            this_selection.append(self.current_node.prev_move)
        
        self.select_order.append(self.current_node.prev_move)
        if Globals.checkWinGrid(self.major_grid, self.current_node.prev_move[0]):
            pass
        if self.depth > 50:
            pass
        Globals.updateMajorGrid(self.major_grid, self.current_state, self.current_node.prev_move, self.possible_moves)


    """mcts always starts with player = 1 since thats designated by game
            make its move then swap.
            then make enemy move and swap
            no need to swap at expansion since its done here"""


    """def generate_valid_move(self, prev_move):
        if self.possible_moves[prev_move[1]]:
            return prev_move[1], random.choice(self.possible_moves[prev_move[1]])
        else:
            gen = random.choice()


            while the first move generated randomly is empty, keep generating till not

            this is regarding expansion
            what do if near end game and no more valid moves
            have to re-select
            do something to make the move not explored as much
            if node is win, then just add it?
            and if its loss then just do that?
            ig?
            so the simulation would need to be altered to first check if its already a game-ender"""


        
    def expansion(self):
        # some problem with expansion allows generating children from moves not in the possible moves
        if len(self.possible_moves[self.prev_move[1]]) > 0:
            move1 = self.prev_move[1]
            for move2 in self.possible_moves[self.prev_move[1]]:
                self.current_node.children.append(Node((move1, move2), parent=self.current_node))

            # move = self.prev_move[1], random.choice(self.possible_moves[self.prev_move[1]])
            # self.prev_move = move
        elif Globals.checkWinGrid(self.major_grid, self.prev_move[0]) is not None:
            # is current node a leaf node, if so keep at leaf node
            self.player = Globals.swap(self.player) # is this correct?
            return None
        
        elif self.major_grid[self.prev_move[1]] in Globals.winners:
            for move1 in range(len(self.possible_moves)):
                for move2 in self.possible_moves[move1]:
                    self.current_node.children.append(Node((move1, move2), parent=self.current_node))

        else:
            print("lineage")
            print(self.current_node.get_lineage())
            pass

        self.depth += 1

        if self.depth >= len(self.all_children_selections):
            self.all_children_selections.append({})

        for child_node in self.current_node.children:
                self.all_children_selections[self.depth][child_node.prev_move] = 0
            
        child = random.choice(self.current_node.children)

        self.all_children_selections[self.depth][child.prev_move] += 1

        self.prev_move = child.prev_move

        if self.prev_move[1] not in self.possible_moves[self.prev_move[0]]:
            pass
        elif self.prev_move[0] == 4:
            pass
        self.possible_moves[self.prev_move[0]].remove(self.prev_move[1])

        # here add a UTC calculator?

        self.current_state[child.prev_move[0]][child.prev_move[1]] = Globals.winners[self.player]

        # updateGameState only checks for minor grid win using prev_move and updates major grid

        Globals.updateMajorGrid(self.major_grid, self.current_state, self.prev_move, self.possible_moves)

        self.current_node = child
        
    
    """self.current_node = child
    
    update current state

    update major grid, check win
    what about if node doesnt have valid children"""
        
    # better way to find random valid move than while loop
    # what to do when expanding a terminal node
        # or selecting a terminal node
        # when expanding can make simulate just return the result, and back propogate it
        # when selecting, can make expand just return the node by checking win
     # this would mean i can select terminal nodes, and back propagate them
    # is that fine

    # need to make utc finder find the minimal or maximal depending on player

    def simulation(self):
        result = Globals.checkWinGrid(self.major_grid, self.prev_move[0])

        if result is None:
            sim_state = copy.deepcopy(self.current_state)
            sim_possible_moves = copy.deepcopy(self.possible_moves)
            sim_major_grid = self.major_grid[:]
            prev_move = self.current_node.prev_move[:]
            player = Globals.swap(self.player)
        else:
            pass
            # self.player = Globals.swap(self)   <-- solution to current bug of not in possible_moves

        while result is None:

            if sim_possible_moves[prev_move[1]]:
                prev_move = prev_move[1], random.choice(sim_possible_moves[prev_move[1]])
            else:
                move1 = random.randrange(0,9)
                while not sim_possible_moves[move1]:
                    move1 = random.randrange(0,9)
                prev_move = move1, random.choice(sim_possible_moves[move1])
            

            sim_state[prev_move[0]][prev_move[1]] = Globals.winners[player]
            # updateGameState = checkminor grid win using prev_move, if won removes possible moves there
            Globals.updateMajorGrid(sim_major_grid, sim_state, prev_move, sim_possible_moves)

            # print(prev_move)
            # print(sim_possible_moves)

            

            result = Globals.checkWinGrid(sim_major_grid, prev_move[0])

            player = Globals.swap(player)

        return result
    

    def printGrid(self, current_state):
        # print physical grid

        print("-" * 12)
        for m in range(3):
            for i in range(3):
                row = "|"
                for d in range(3):
                    d = d + 3 * m
                    for c in range(3):
                        c = c  + 3 * i
                        row += current_state[d][c]
                    row += "|"
                print(row)
            print("-" * 12)
    
    # result should be +ve if the winner is the current player
    # -ve if the winner is the other player other than the one initiating from node
    # can keep track of current player while selecting

    def backpropogation(self, result):
        if self.player == result:
            self.current_node.win += 1
        else:
            self.current_node.win -= 1
        self.current_node.sim += 1


        while self.current_node.parent is not None:
            self.player = Globals.swap(self.player)
            if result == self.player:
                self.current_node.parent.win += 1
            else:
                self.current_node.parent.win -= 1

            self.current_node.parent.sim += 1

            self.current_node = self.current_node.parent
        
        self.current_state = copy.deepcopy(self.init_state)
        self.possible_moves = copy.deepcopy(self.init_possible_moves)
        self.major_grid = self.init_major_grid[:]
        self.prev_move = self.init_prev_move[:]
        self.player = self.init_player
        self.depth = 0
        # del player?
    
    def play_out(self, moves):
        self.current_state = copy.deepcopy(self.init_state)
        self.possible_moves = copy.deepcopy(self.init_possible_moves)
        self.major_grid = self.init_major_grid[:]
        self.prev_move = self.init_prev_move[:]
        self.player = 1

        for move in moves:
            self.prev_move = move
            self.current_state[move[0]][move[1]] = Globals.winners[self.player]
            self.possible_moves[self.prev_move[0]].remove(self.prev_move[1])
            Globals.updateMajorGrid(self.major_grid, self.current_state, self.prev_move, self.possible_moves)
            self.player = Globals.swap(self.player)
            self.printGrid(self.current_state)
            print(self.prev_move)
            pass
        pass

    def tree_search(self):
        max_iterations = 6000
        i = 0
        test_moves = [(4, 1), (1, 7), (7, 1), (1, 3), (3, 8), (8, 4), (4, 0), (0, 8), (8, 6), (6, 5), (5, 2), (2, 4), (4, 6), (6, 3), (3, 0), (0, 2), (2, 6), (6, 1), (1, 4), (4, 2), (2, 1), (1, 1), (1, 2), (2, 5), (5, 6), (6, 2), (2, 3), (3, 6), (6, 8), (8, 2), (2, 7), (7, 3), (3, 5), (5, 5), (5, 1), (1, 5), (5, 4), (4, 5), (4, 3), (3, 3), (3, 2)]
        # self.play_out(test_moves)
        while i < max_iterations:
            # print("start iteration")
            self.selection()

            # print("select order:\n", self.select_order)

            self.expansion()
            sim_result = self.simulation()
            self.backpropogation(sim_result)

            i += 1
            if i == max_iterations - 1:
                pass
        
        self.find_all_node_data(0, self.current_node)
        # self.display_all_node_data()

        for depth in range(len(self.all_node_data)):
            print("depth: {}, nodes: {}".format(depth, len(self.all_node_data[depth])))

        outputFile = open("outputdata.pkl", 'wb')
        pickle.dump(self.all_node_data, outputFile)
        outputFile.close()

        
        # display_all_children_selections(self.all_children_selections)

        # self.find_all_UTCs(0, self.current_node)
        # self.display_all_UTCs()
        # self.display_all_UTC_totals()
        return random.choice(self.find_best_UTC(self.root.children))


    def find_all_node_data(self, depth, node):
        if depth >=  len(self.all_node_data):
            self.all_node_data.append({})
        self.all_node_data[depth][node] = [node.prev_move, node.win, node.sim, node.UTC]

        for child in node.children:
            self.find_all_node_data(depth + 1, child)
    
    def display_all_node_data(self):
        for depth in range(len(self.all_node_data)):
            print("depth: {}".format(depth))
            for node in self.all_node_data[depth].keys():
                print(self.all_node_data[depth][node], end=", ")
            print()

    # def find_all_UTCs(self, depth, node):
    #     if depth >= len(self.all_UTC_values):
    #         self.all_UTC_values.append({})

    #     self.all_UTC_values[depth][node.prev_move] = node.UTC

    #     for child in node.children:
    #         self.find_all_UTCs(depth+1, child)
        
    # def display_all_UTCs(self):
    #     print("\nall UTC values: \n")
    #     for depth in range(len(self.all_UTC_values)):
    #         print("depth {}".format(depth))
    #         print(self.all_UTC_values[depth])

    # def display_all_UTC_totals(self):
    #     for i in range(len(self.all_children_selections) + 1):
    #         total = 0
    #         for utc in self.all_UTC_values[i]:
    #             total += utc
    #         print("self.depth: {}, total: {}".format(i, total))
    # self.player still swapping

    # expand all child nodes, then choose one at random to select
    # this means dont need to recalculate UTC values at back-propogation stage
    # since doing at for selection, to update UTC between siblings?

    # have to recalculate UTC at selection
    # particularly if UTC changes if parent simulations num changes
    
    """def update_local_variables(self, game_state, major_grid, possible_moves, prev_move):
        self.current_state = game_state
        self.major_grid = major_grid
        self.possible_moves = possible_moves
        self.prev_move = prev_move

        self.root = Node(self.prev_move)
        self.generate_root_children()

    ???"""

    # def test(self):
    #     return None
    #     if not self.possible_moves[self.current_node.prev_move[0]]:
    #         pass

    # def testing(self):
    #     while True:
    #         self.major_grid = [' ', ' ', ' ', ' ', ' ', 'O', ' ', ' ', ' ']
    #         self.possible_moves = [[1, 5, 6, 8], [0, 3, 4, 8], [7, 8], [0, 1, 4, 5, 6, 8], [1, 3, 8], [], [0, 2, 3, 6, 7, 8], [3, 4, 6], [0, 2, 3, 4, 5, 6, 7, 8]]
    #         self.current_state = [['X', ' ', 'O', 'O', 'O', ' ', ' ', 'X', ' '], [' ', 'X', 'O', ' ', ' ', 'X', 'O', 'O', ' '], ['O', 'X', 'O', 'O', 'X', 'O', 'X', ' ', ' '], [' ', ' ', 'X', 'X', ' ', ' ', ' ', 'O', ' '], ['X', ' ', 'X', ' ', 'O', 'O', 'O', 'X', ' '], ['X', 'O', 'X', ' ', 'O', ' ', ' ', 'O', ' '], [' ', 'O', ' ', ' ', 'X', 'X', ' ', ' ', ' '], ['O', 'O', 'X', ' ', ' ', 'X', ' ', 'X', 'O'], [' ', 'X', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]
    #         self.prev_move = (7,5)
    #         self.player = 1
    #         self.current_node = Node(self.prev_move)

    #         self.expansion()

    #         if not self.possible_moves[self.current_node.prev_move[0]]:
    #             pass


    #     pass
        

    # def add_node(self, node, player):
    #     self.prev_move = node.prev_move
    #     self.current_state[self.prev_move[0]][self.prev_move[1]] = Globals.winners[player]
        
    #     self.possible_moves[self.prev_move[0]].remove(self.prev_move[1])






    
        
    
    # have to +/- 1 on differing turns, depending on who's turn that move is
    

            

        # sim_possible_moves - node.prev_move
        
    # copy current_state, possible_moves
    

    

    


    # see that everything is updated correctly
    # all data structures
    # for many runs
    # look at edge cases, i.e. when grids are full, when terminal node


def display_all_children_selections(all_children_selections):
    for depth in range(len(all_children_selections)):
        print("self.depth: {}".format(depth))
        print(all_children_selections[depth])


# i need to initialise the first child nodes with the UTC value
# whenever I generate a child node, i need to calculate its UTC
# otherwise UTC is only updated by selecting a node then backpropogating it
# it wont update its siblings.