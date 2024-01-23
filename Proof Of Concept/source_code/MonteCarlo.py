import Node
import random
import math
import Globals

class MonteCarlo:
    def __init__(self, current_state, major_grid, possible_moves) -> None:
        self.root = Node((-1,-1), self.root)
        self.current_state = current_state
        self.major_grid = major_grid
        self.possible_moves = possible_moves
        self.starting_player = 0

        self.C = math.log(2)

        self.generate_root_children()
    
    def generate_root_children(self):
        for move in self.possible_moves:
            self.root.children.append(Node(move, self.root))
        

    def find_best_UTC(self, nodes):
        best = [Node((-1,-1), self.root)]
        best[0].UTC = 0

        for node in nodes:
            if node.UTC == best[0].UTC:
                best.append(node)
            if node.UTC > best[0].UTC:
                best = [node]
        
        return best
    
    def selection(self):
        # if current state has no children:
        # return the state
        # if it has children, current=child which maximises UTC formula
        # update current_state, and possible moves to confirm the selection

        # root starts as having all its children expanded.
        current = self.root
        current_player = self.starting_player


        if not current.children:
            return (current, current_player)
        else:
            current = random.choice(self.find_best_UTC(current.children))
            current_player = Globals.swap(current_player)

            Globals.updateGameState(self.current_state, current.prev_move, self.major_grid, self.possible_moves)


    def get_valid_moves(self, prev_move):
        if self.possible_moves[prev_move[1]]:
            return self.possible_moves
        else:
            return self.possible_moves[prev_move[1]]
        
    def expansion(self, node):
        move = random.choice(self.get_valid_moves(node.prev_move))
        child = Node(prev_move=move, parent=node)

        self.possible_moves.remove(move)
        node.children.append(child)
        return child
    
    # update major grid, check win
    # update current state

    def simulation(self, node, player):
        sim_state = self.current_state
        sim_possible_moves = self.possible_moves
        sim_major_grid = self.major_grid
        prev_move = node.prev_move

        result = None

        while result is None:
            if sim_possible_moves[prev_move[1]]:
                prev_move = random.choice(sim_possible_moves)
            else:
                prev_move = random.choice(sim_possible_moves[prev_move[1]])
            
            Globals.updateGameState(sim_state, prev_move, sim_major_grid, sim_possible_moves)
            result = Globals.checkWinGrid(sim_major_grid)
        
        return result
    
    # result should be +ve if the winner is the current player
    # -ve if the winner is the other player other than the one initiating from node
    # can keep track of current player while selecting

    def backpropogation(self, node, result):
        node.win += result
        node.sim += 1

        while node.parent is not node:
            node.parent.win += result
            node.parent.sim += 1

            node.UTC = UTC_calculate(node)

            node = node.parent
    

    def tree_search(self):

    
        
    
    # have to +/- 1 on differing turns, depending on who's turn that move is
    

            

        # sim_possible_moves - node.prev_move
        
    # copy current_state, possible_moves
    

def UTC_calculate(self, a):
        return (a.win / a.loss) + self.C * (math.sqrt(math.log(a.parent.sim) / a.sim))
    

    


    