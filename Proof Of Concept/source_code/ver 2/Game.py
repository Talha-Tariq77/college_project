from Globals import *

import MonteCarlo

class Game:
    def __init__(self) -> None:
        self.current_state = init_state
        self.major_grid = init_major_grid
        self.possible_moves = init_possible_moves
        self.prev_move = init_prev_move
        self.player = starting_player

        self.winner = None

        self.monteCarlo = MonteCarlo.MonteCarlo(self.prev_move, self.current_state, self.major_grid, self.possible_moves, self.player)

    def printGrid(self):
        # print physical grid

        print("-" * 12)
        for m in range(3):
            for i in range(3):
                row = "|"
                for d in range(3):
                    d = d + 3 * m
                    for c in range(3):
                        c = c  + 3 * i
                        row += self.current_state[d][c]
                    row += "|"
                print(row)
            print("-" * 12)
        
    def checkAskMoveA(self):
        """
        checks if move A needs to be asked for
        - if the previous move [A]'s grid has valid moves
        returns False
        otherwise, since player can play anywhere, returns False
        """
        if self.prev_move == init_prev_move:
            return True
        elif not self.possible_moves[self.prev_move[1]]:
            return True
        else:
            return False
    
    def checkValidMoveA(self, moveA):
        """
        checks if moveA is a syntactically valid and possible move"""
        if moveA in correct_move_inputs:
            if self.possible_moves[int(moveA) - 1]:
                return True
            
        return False
    
    def checkValidMoveB(self, moveA, moveB):
        if moveB in correct_move_inputs:
            if int(moveB) - 1 in self.possible_moves[moveA]:
                return True
            
        return False
    
    # def getValidMoves(self):
    #     if self.prev_move is None:
    #         return possible_moves
    #     elif not self.current_state[self.prev_move[1]]:
    #         return possible_moves
    #     else:
    #         return possible_moves[self.prev_move[1]]
        
    def getPlayerMove(self):

        if self.checkAskMoveA():
            a = input("Player %s's Move Grid: " % self.player)

            while not self.checkValidMoveA(a):
                print("Invalid Input")
                a = input("Player %s's Move Grid: " % self.player)
            
            a = int(a) - 1

        else:
            a = self.prev_move[1]
        
        b = input("Player %s's Move Value: " % self.player)
        
        while not self.checkValidMoveB(a, b):
            print("Invalid Input")
            b = input("Player %s's Move Value: " % self.player)



        return (a, int(b)-1)

    
    def run(self):
        # these are *global* variables from another file, being reassigned here
        # but python assumes all variables 'declared' in a function are local variables
        # to break this assumption, these variables must be declared as global
        result = None
        
        while result is None:

            self.printGrid()

            if self.player == 0:
                self.prev_move = self.getPlayerMove()
            
            else:
                self.monteCarlo.__init__(self.prev_move, self.current_state, self.major_grid, self.possible_moves, self.player)
                node = self.monteCarlo.tree_search()
                self.prev_move = node.prev_move
                # need to re-iniate MCTS class with new initial variables

            
            add_move(self.current_state, self.prev_move,self.possible_moves, self.player)
                
            if updateMajorGrid(self.major_grid, self.current_state, self.prev_move, self.possible_moves):
                result = checkWinGrid(self.major_grid, self.prev_move[0])

            # when adding move, add move function -> update major grid seperately
                # prev move already updated, player already updated
                # updates the current_state, major grid, and possible moves

            self.player = swap(self.player)
            
    

game = Game()

game.run()

    # grid = self.prev_move[0]
    # value = self.prev_move[1]
    # # check current_grid
    # for check_line in check_lines[value]:
    #     current_line = ""
    #     for check_value in check_line:
    #         current_line += game_state[grid][check_value]

    #     if current_line in win_loss:
    #         return win_loss.index(line)
    #     # returns winner (O = 0, X=1) or None
    
    # return None





# for i in range(9):

#     result = []

#     for line in possible_checks:
#         if i in line:
#             result.append(line)
#     print("%s: %s," % (i, result))





# notes:

# sim