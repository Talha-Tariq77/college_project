from Globals import *

import MonteCarlo

class Game:
    def __init__(self) -> None:
        self.monteCarlo = MonteCarlo.MonteCarlo(game_state, major_grid, possible_moves)

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
        
    def checkAskMoveA(self):
        """
        checks if move A needs to be asked for
        - if the previous move [A]'s grid has valid moves
        returns False
        otherwise, since player can play anywhere, returns False
        """
        if prev_move is None:
            return True
        elif not possible_moves[prev_move[1]]:
            return True
        else:
            return False
    
    def checkValidMoveA(self, moveA):
        """
        checks if moveA is a syntactically valid and possible move"""
        if moveA in correct_move_inputs:
            if possible_moves[int(moveA) - 1]:
                return True
            
        return False
    
    def checkValidMoveB(self, move):
        """checks if moveB is syntactically valid and possible move"""
        if move[1] in correct_move_inputs:
            if int(move[1]) - 1 in possible_moves[int(move[0])]:
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
            a = input("Player %s's Move Grid: " % current_player)

            while not self.checkValidMoveA(a):
                print("Invalid Input")
                a = input("Player %s's Move Grid: " % current_player)
            
            a = int(a) - 1

        else:
            a = prev_move[1]
        
        b = input("Player %s's Move Value: " % current_player)
        
        while not self.checkValidMoveB((a, b)):
            print("Invalid Input")
            b = input("Player %s's Move Value: " % current_player)

        # valid = False
        # if b in correct_move_inputs:
        #     if valid_moves[int(b)]:
        #         valid = True

        # while not valid:
        #     print("Invalid Input")
        #     b = input("Player %s's Move Value: " % self.current_player)
        #     if b in correct_move_inputs:
        #         if valid_moves[int(b)]:
        #             valid = True
        
        return (a, int(b)-1)

    
    def run(self):
        global prev_move
        global current_player

        # these are *global* variables from another file, being reassigned here
        # but python assumes all variables 'declared' in a function are local variables
        # to break this assumption, these variables must be declared as global
        
        while True:
            if current_player == 0:

                self.printGrid(game_state)

                prev_move = self.getPlayerMove()
                
                add_move(game_state, prev_move)
                
                updateGameState(game_state, prev_move, major_grid, possible_moves)
            
            else:
                self.printGrid(game_state)
                
                node = self.monteCarlo.tree_search()
                prev_move = node.prev_move()

                add_move(game_state, prev_move)

                updateGameState(game_state, prev_move, major_grid, possible_moves)

            
            current_player = swap(current_player)
            
    

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