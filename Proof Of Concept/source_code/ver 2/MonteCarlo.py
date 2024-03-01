from Node import Node
import random
import math
import Globals

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
    
    def generate_root_children(self):
        if self.prev_move == (-1,-1) or not self.possible_moves[self.prev_move[1]]:
            for x in range(len(self.possible_moves)):
                for y in self.possible_moves[x]:
                    self.root.children.append(Node((x,y), self.root))
        else:
            for x in self.possible_moves[self.prev_move[1]]:
                self.root.children.append(Node((self.root.prev_move[1], x), self.root))
            
    def UTC_calculate(self, a):
        return (a.win / a.sim) + self.C * (math.sqrt(math.log(a.parent.sim) / a.sim))
        

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
        depth = 0
        while self.current_node.children:
            depth += 1
            self.current_node = random.choice(self.find_best_UTC(self.current_node.children))

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
        if depth > 50:
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
        result = Globals.checkWinGrid(self.major_grid, self.prev_move[0])
        if result is not None:
            self.player = Globals.swap(self.player)
            return result 
        elif Globals.checkWinGridFull(self.current_state[self.prev_move[1]]) is not None:
            choose_from = []
            for i in range(len(self.possible_moves)):
                if len(self.possible_moves[i]) > 0:
                    choose_from.append(i)

            move1 = random.choice(choose_from)

                # what to do if empty
                # better way to generate when more full - look at major grid, or possible moves values not equal to [], when choosing randomly
    

            move2 = random.choice(self.possible_moves[move1])

            move = move1, move2
            self.prev_move = move
            # print("brancha", move)
            # branch a at fault

        elif len(self.possible_moves[self.prev_move[1]]) > 0:
            move = self.prev_move[1], random.choice(self.possible_moves[self.prev_move[1]])
            self.prev_move = move
            # print("branchb", move)
        else:
            print("lineage")
            print(self.current_node.get_lineage())
            pass

#         if len(self.possible_moves[self.current_node.prev_move[1]]) > 0:
#             move = self.current_node.prev_move[1], random.choice(self.possible_moves[self.current_node.prev_move[1]])
#             if self.current_node.prev_move[0] == 4:
#                 pass

# # check win of grid 
#         elif Globals.updateMajorGrid(self.major_grid, self.current_state, self.current_node.prev_move, self.possible_moves) is not None:
#             self.prev_move = self.current_node.prev_move
#             if self.current_node.prev_move[0] == 4:
#                 pass
#             print("lineage")
#             print(self.current_node.get_lineage())
#             return 1
#         else:
#             # if self.major_grid == ["D" for i in range(9)]:
#             choose_from = []
#             for i in range(len(self.possible_moves)):
#                 if len(self.possible_moves[i]) > 0:
#                     choose_from.append(i)

#             move1 = random.choice(choose_from)

#                 # what to do if empty
#                 # better way to generate when more full - look at major grid, or possible moves values not equal to [], when choosing randomly
    

#             move2 = random.choice(self.possible_moves[move1])

#             move = move1, move2
        
        if self.prev_move[1] not in self.possible_moves[self.prev_move[0]]:
            pass
        elif self.prev_move[0] == 4:
            pass

        # move = random.choice(self.get_valid_moves(node.prev_move))
        child = Node(prev_move=self.prev_move, parent=self.current_node)

        self.possible_moves[self.prev_move[0]].remove(self.prev_move[1])

        self.current_node.children.append(child)

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

            self.current_node.UTC = self.UTC_calculate(self.current_node)

            self.current_node = self.current_node.parent
        
        self.current_state = copy.deepcopy(self.init_state)
        self.possible_moves = copy.deepcopy(self.init_possible_moves)
        self.major_grid = self.init_major_grid[:]
        self.prev_move = self.init_prev_move[:]
        self.player = self.init_player
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
        max_iterations = 1500
        i = 0
        test_moves = [(4, 1), (1, 7), (7, 1), (1, 3), (3, 8), (8, 4), (4, 0), (0, 8), (8, 6), (6, 5), (5, 2), (2, 4), (4, 6), (6, 3), (3, 0), (0, 2), (2, 6), (6, 1), (1, 4), (4, 2), (2, 1), (1, 1), (1, 2), (2, 5), (5, 6), (6, 2), (2, 3), (3, 6), (6, 8), (8, 2), (2, 7), (7, 3), (3, 5), (5, 5), (5, 1), (1, 5), (5, 4), (4, 5), (4, 3), (3, 3), (3, 2)]
        # self.play_out(test_moves)

        while i < max_iterations:
            # print("start iteration")
            self.selection()
            # print("select order:\n", self.select_order)

            expansion_result = self.expansion()
            if expansion_result is not None:
                self.backpropogation(expansion_result)
            else:
                sim_result = self.simulation()
                self.backpropogation(sim_result)

            i += 1
            if i == max_iterations - 1:
                pass
        
        return random.choice(self.find_best_UTC(self.root.children))
    
    # self.player still swapping
    
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
    

    

    


    