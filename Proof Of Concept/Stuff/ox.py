import random


class Game:
    def __init__(self):
        self.grid = [['#', '#', '#'], ['#', '#', '#'], ['#', '#', '#']]
        self.player1 = 'Talha'
        self.player2 = 'AI'
        self.symbols = ['X', 'O']
        self.winner = None
        self.turn = 0
        #self.record = open('oxinfo.txt', 'a')
        self.possible = self.get_possible()
        self.moves = []
        self.condition = None
        self.current_player = self.turn
        self.tree = []

    def display_grid(self):
        for row in self.grid:
            for value in row:
                print(value, end='')
            print()
        print()

    def play(self, mode=0):

        while self.condition not in ['DRAW', 'WIN']:
            self.current_player = self.turn % 2

            self.display_grid()

            self.make_move(mode)

            #if self.current_player == 0:
                #self.temp_record.append(coordinates)
            #print(self.temp_record)

            self.turn += 1
            #print('record: ', self.temp_record)

            self.winner, self.condition = self.check_win(self.grid)

        self.display_grid()
        print(self.winner)
        print(self.condition)
        #self.record_moves()

    def make_move(self, mode):
        print('Player {} - {}'.format(str(self.current_player + 1), self.symbols[self.current_player]))

        coordinates = self.get_coordinates(mode)
        y, x = coordinates

        self.grid[x][y] = self.symbols[self.current_player]
        self.possible.remove(coordinates)
        print('new func', self.get_possible_properly(self.grid))

        if self.current_player == 0:
            self.moves.append(coordinates)

        # print(self.possible)
        # print(self.moves)

    def get_coordinates(self, mode):
        if mode == 0:
            if self.current_player == 0:  # Perform evaluation only for player 1 or for player 2 aswell?
                reccomended = self.evaluate_moves()
                if reccomended:
                    return reccomended

            return random.choice(self.possible)

        else:
            coordinates = input('coordinates: ')
            coordinates = int(coordinates[0]), int(coordinates[1])
            while coordinates not in self.possible:
                print('Error: This coordinate is occupied')
                coordinates = input('coordinates: ')
                coordinates = int(coordinates[0]), int(coordinates[1])

            return coordinates

        # if player == 0:
        #     self.temp_record.append(coordinates)
        # print(self.temp_record)

    def check_win(self, grid):
        for row in self.get_winners(grid):
            for i in range(len(self.symbols)):
                if row == [game.symbols[i]] * 3:
                    return i + 1, 'WIN'

        if self.board_filled(grid):
            return random.randint(0, 1), 'DRAW'
        else:
            return None, None

    def board_filled(self, grid):
        for row in grid:
            if ' ' in row:
                return False
        return True

    def get_winners(self, grid):
        winners = []
        # horizontal
        for x in range(len(grid)):
            winners.append(grid[x])
        
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

    # def record_moves(self):
    #     for coord in self.temp_record:
    #         self.record.write('{},{} '.format(coord[0], coord[1]))
    #     self.record.write('winner: ' + str(self.winner) + '\n')
    #     self.record.close()

    def get_possible(self):
        possible = []
        for row in range(len(self.grid)):
            for col in range(len(self.grid)):
                possible.append((col, row))
        return possible

    def evaluate_moves(self):
        temp_grid = [x[:] for x in self.grid]  # list1 = list2, any modifications to list1 will modify list2,
                                     # so use list1 = list2.copy() or list(list2)
        points = {}

        for coordinate in self.possible:
            y, x = coordinate
            temp_grid[x][y] = self.symbols[0]

            winner, condition = self.check_win(temp_grid)  # something fishy here
            if winner == 1 and condition == 'WIN':
                points[coordinate] = 10
            else:
                points[coordinate] = 0
            temp_grid = [x[:] for x in self.grid]

        print(points)
        points = sorted((value, coord) for (coord, value) in points.items())
        print(points)
        for score in points:
            for i in range(len(score)):
                val, co = score
                if val >= 10:
                    return co
        return None

    def get_possible_properly(self, grid):
        poss = []
        for row in range(len(grid)):
            for col in range(len(grid)):
                if grid[row][col] == '#':
                    poss.append((col, row))
        return poss

    def get_game_tree(self):
        for coordinate in self.get_possible_properly(self.grid):
            pass


    def eval(self, temp_grid):
        if len(self.get_possible_properly(temp_grid)) >= 1:
            for coordinate in self.get_possible_properly(temp_grid):
                x, y = coordinate
                print('dsfgds', temp_grid, [x[:] for x in temp_grid])
                temp_grid[x][y] = self.symbols[self.turn % 2]
                self.turn += 1

        winner, condition = self.check_win(temp_grid)  # something fishy here
        if winner == 1 and condition == 'WIN':
            return 10
        elif condition == 'DRAW':
            return 0
        elif winner == 0 and condition == 'WIN':
            return -10
        else:
            return eval(temp_grid)


# not correct number being recorded. why
# multi-game, repeating system

record = {}
grids = []
conditions = []
game = Game()
print(game.grid)
print(game.eval([x[:] for x in game.grid]))

# number_of_games = 1
#
# for i in range(number_of_games):
#     game.play(0)
#     record[i] = game.moves
#     grids.append(game.grid)
#     conditions.append((game.winner, game.condition))
#     game.__init__()
#
# if number_of_games > 3:
#     print('RECORD:')
#     for i in range(number_of_games):
#         if conditions[i][1] == 'DRAW':
#             print()
#             print(record[i])
#             game.grid = grids[i]
#             game.display_grid()
#             print(conditions[i])


'''
Note:
No continuity in:
>order of coordinates- always accurate,
>player value: 0 or 1 – only 1 in display, otherwise 0
'''


