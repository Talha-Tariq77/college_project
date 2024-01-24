import math
import random

game_state = [[" "," "," ", " "," "," ", " "," "," "],[" "," "," ", " "," "," ", " "," "," "],[" "," "," ", " "," "," ", " "," "," "],
              [" "," "," ", " "," "," ", " "," "," "],[" "," "," ", " "," "," ", " "," "," "],[" "," "," ", " "," "," ", " "," "," "],
              [" "," "," ", " "," "," ", " "," "," "],[" "," "," ", " "," "," ", " "," "," "],[" "," "," ", " "," "," ", " "," "," "]]

winners = ["O", "X", "D"]
win_loss = ["OOO", "XXX"]

correct_move_inputs = [str(i) for i in range(1, 10)]

# possible_checks = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]


check_lines = {0: [[0, 1, 2], [0, 3, 6], [0, 4, 8]],
                  1: [[0, 1, 2], [1, 4, 7]],
                  2: [[0, 1, 2], [2, 5, 8], [2, 4, 6]],
                  3: [[3, 4, 5], [0, 3, 6]],
                  4: [[3, 4, 5], [1, 4, 7], [0, 4, 8], [2, 4, 6]],
                  5: [[3, 4, 5], [2, 5, 8]],
                  6: [[6, 7, 8], [0, 3, 6], [2, 4, 6]],
                  7: [[6, 7, 8], [1, 4, 7]],
                  8: [[6, 7, 8], [2, 5, 8], [0, 4, 8]]
                  }
# for each of the prev_move locations, the associated checks

possible_moves = [[0,1,2,3,4,5,6,7,8] for x in range(9)]

major_grid = [" "] * 9

# the won/loss grid

prev_move = None

current_player = 0


def checkWinGrid(grid, prev_move):
    # prev move is prev_move[1] here, grid is local grid
    # returns 0 if 0 won, 1 if 1 won the grid, 2 if its a draw, 0 otherwise
    for line in check_lines[prev_move]:
        current_check = ""
        for value in line:
            current_check += grid[value]
        
        if current_check in win_loss[:2]:
            return win_loss.index(current_check)
    
    if " " not in grid:
        return 2
    # i.e. if no win/loss and not empty, draw
    else:
        return None


# def updateMajorGrid(self, major_grid, major_grid_self.prev_move):
#     return self.updateMinorGrid(major_grid[major_grid_self.prev_move[0]])

        # major_grid[major_grid_self.prev_move[0]] = winners.index(currentMinorResult)
        
    

def updateGameState(game_state, prev_move, major_grid, possible_moves):
    # updates the Major Grid, checking result of prev_move's grid
    # removes possible moves of the local grid if grid is terminated

    # major_grid = [" "*9], win/loss grid
    # current_state = actual current state, all local grids

    currentMinorResult = checkWinGrid(game_state[prev_move[0]], prev_move[1])
    # check if the previous_move's grid has won/loss

    if currentMinorResult is not None:
        major_grid[prev_move[0]] = winners[currentMinorResult]

        possible_moves[prev_move[0]] = []
        # won/loss/drawn grid no longer has any possible moves

def add_move(game_state, prev_move):
    game_state[prev_move[0]][prev_move[1]] = winners[current_player]
    possible_moves[prev_move[0]].remove(prev_move[1])
    # move = random.choice(self.get_valid_moves(node.prev_move))


def swap(player):
    if player == 0:
        return 1
    elif player == 1:
        return 0
    else:
        raise TypeError("Only 1 or 0 allowed")
# when changing a singular variable must return
# allowed to change inputted data structures but not inputted singular varaibles



# globals as game.py locals