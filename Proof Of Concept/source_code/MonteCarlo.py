from Node import Node
import random
import math
import Globals

import copy

class MonteCarlo:
    def __init__(self, prev_move, init_state, init_major_grid, possible_moves, player) -> None:
        self.prev_move = None
        self.root = Node((-1,-1))
        self.current_state = None
        self.major_grid = None
        self.possible_moves = None
        self.starting_player = 0

        self.C = math.log(2)
    
    def generate_root_children(self):
        if self.possible_moves[self.root.prev_move[0]]:
            for x in self.possible_moves[self.prev_move[0]]:
                self.root.children.append(Node((self.root.prev_move[0], x), self.root))

        else:
            for x in range(len(self.possible_moves)):
                for y in self.possible_moves[x]:
                    self.root.children.append(Node((x,y), self.root))

        pass

    def UTC_calculate(self, a):
        return (a.win / a.sim) + self.C * (math.sqrt(math.log(a.parent.sim) / a.sim))
        

    def find_best_UTC(self, nodes):
        best_nodes = [nodes[0]]

        for node in nodes[1:]:
            if node.UTC == best_nodes[0].UTC:
                best_nodes.append(node)

            if node.UTC > best_nodes[0].UTC:
                best_nodes = [node]
        
        return best_nodes
    
    def selection(self):
        # if current state has no children:
        # return the state
        # if it has children, current=child which maximises UTC formula
        # update current_state, and possible moves to confirm the selection

        # root starts as having all its children expanded.
        current = self.root
        current_player = self.starting_player


        while current.children:
            current = random.choice(self.find_best_UTC(current.children))
            current_player = Globals.swap(current_player)

            if self.possible_moves[current.prev_move[0]]:
                self.possible_moves[current.prev_move[0]].remove(current.prev_move[1])

            self.current_state[current.prev_move[0]][current.prev_move[1]] = Globals.winners[current_player]
            Globals.updateGameState(self.current_state, current.prev_move, self.major_grid, self.possible_moves)

            self.prev_move = current.prev_move

        return (current, current_player)
    

    def generate_valid_move(self, prev_move):
        if self.possible_moves[prev_move[1]]:
            return prev_move[1], random.choice(self.possible_moves[prev_move[1]])
        else:
            gen = random.choice()
            # while the first move generated randomly is empty, keep generating till not

            # this is regarding expansion
            # what do if near end game and no more valid moves
            # have to re-select
            # do something to make the move not explored as much
            # if node is win, then just add it?
            # and if its loss then just do that?
            # ig?

            # so the simulation would need to be altered to first check if its already a game-ender

        
    def expansion(self, node, player):
        if self.possible_moves[node.prev_move[1]]:
            move = node.prev_move[1], random.choice(self.possible_moves[node.prev_move[1]])
        else:
            # if self.major_grid == ["D" for i in range(9)]:
            move1 = random.randrange(0,9)
            while not self.possible_moves[move1]:
                # i.e. empty
                move1 = random.randrange(0,9)

            move2 = random.choice(self.possible_moves[move1])

            move = move1, move2
        
        self.prev_move = move

        # move = random.choice(self.get_valid_moves(node.prev_move))
        child = Node(prev_move=self.prev_move, parent=node)

        self.possible_moves[move[0]].remove(move[1])
        node.children.append(child)

        self.current_state[child.prev_move[0]][child.prev_move[1]] = Globals.winners[Globals.swap(player)]

        # updateGameState only checks for minor grid win using prev_move and updates major grid

        Globals.updateGameState(self.current_state, child.prev_move, self.major_grid, self.possible_moves)

        return child
    
    # update current state

    # update major grid, check win
    # what about if node doesnt have valid children

    def simulation(self, node, player):
        sim_state = copy.deepcopy(self.current_state)
        sim_possible_moves = copy.deepcopy(self.possible_moves)
        sim_major_grid = self.major_grid[:]
        prev_move = node.prev_move[:]

        result = None

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
            Globals.updateGameState(sim_state, prev_move, sim_major_grid, sim_possible_moves)

            print(prev_move)
            print(sim_possible_moves)
            if sim_possible_moves[prev_move[0]]:
                sim_possible_moves[prev_move[0]].remove(prev_move[1])

            result = Globals.checkWinGrid(sim_major_grid, prev_move[0])

            self.printGrid(sim_state)

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

    def backpropogation(self, node, result, node_player):
        if node_player == result:
            node.win += 1
        else:
            node.win -= 1
        node.sim += 1

        while node.parent is not None:
            node_player = Globals.swap(node_player)
            if result == node_player:
                node.parent.win += 1
            else:
                node.parent.win -= 1

            node.parent.sim += 1

            node.UTC = self.UTC_calculate(node)

            node = node.parent
    

    def tree_search(self):
        max_iterations = 1500
        i = 0

        while i < max_iterations:
            selected_node, current_player = self.selection()
            
            selected_node_child = self.expansion(selected_node, current_player)


            sim_result = self.simulation(selected_node_child, current_player)

            self.backpropogation(selected_node_child, sim_result, current_player)

            i += 1
        
        return self.find_best_UTC(self.root.children)
    
    def update_local_variables(self, game_state, major_grid, possible_moves, prev_move):
        self.current_state = game_state
        self.major_grid = major_grid
        self.possible_moves = possible_moves
        self.prev_move = prev_move

        self.root = Node(self.prev_move)
        self.generate_root_children()

    
    def add_node(self, node, player):
        self.prev_move = node.prev_move
        self.current_state[self.prev_move[0]][self.prev_move[1]] = Globals.winners[player]
        
        self.possible_moves[self.prev_move[0]].remove(self.prev_move[1])






    
        
    
    # have to +/- 1 on differing turns, depending on who's turn that move is
    

            

        # sim_possible_moves - node.prev_move
        
    # copy current_state, possible_moves
    

    

    


    