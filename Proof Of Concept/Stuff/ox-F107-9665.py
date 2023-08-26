import random


class Game:
    def __init__(self):
        self.grid = [['#', '#', '#'], ['#', '#', '#'], ['#', '#', '#']]
        self.player1 = 'Talha'
        self.player2 = 'AI'
        self.symbols = ['X', 'O']
        self.current_player = None
        self.winner = None
        self.turn = 0
        # self.record = open('oxinfo.txt', 'a')
        self.possible = self.get_possible()
        self.moves = []
        self.condition = None

    def display_grid(self):
        for row in self.grid:
            for value in row:
                print(value, end='')
            print()
        print()

    def play(self, mode=0):

        while self.condition not in ['DRAW', 'WIN']:
            current_player = self.turn % 2

            self.display_grid()

            self.make_move(mode, current_player)

            # if current_player == 0:
            # self.temp_record.append(coordinates)
            # print(self.temp_record)

            self.turn += 1
            # print('record: ', self.temp_record)

            self.winner, self.condition = self.check_win(self.grid)

        self.display_grid()
        print(self.winner)
        print(self.condition)
        # self.record_moves()

    def make_move(self, mode, current_player):
        print('Player {} - {}'.format(str(current_player + 1), self.symbols[current_player]))

        coordinates = self.get_coordinates(mode)
        y, x = coordinates

        self.grid[x][y] = self.symbols[current_player]
        self.possible.remove(coordinates)

        if current_player == 0:
            self.moves.append(coordinates)

        print(self.possible)
        print(self.moves)

    def get_coordinates(self, mode):
        if mode == 0:
            coordinates = random.choice(self.possible)
            self.evaluate_moves()

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
            if '#' in row:
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
        temp_grid = self.grid
        points = {}

        for coordinate in self.possible:
            x, y = coordinate
            temp_grid[x][y] = self.symbols[0]
            winner, self.condition = self.check_win(temp_grid)  # something fishy here
            if winner and self.condition == 'WIN':
                points[coordinate] = 10
            else:
                points[coordinate] = 0
            temp_grid = self.grid
        print(points)


# not correct number being recorded. why
# multi-game, repeating system

record = {}
grids = []
conditions = []
game = Game()

number_of_games = 1

for i in range(number_of_games):
    game.play(0)
    record[i] = game.moves
    grids.append(game.grid)
    conditions.append((game.winner, game.condition))
    game.__init__()

if number_of_games > 3:
    print('RECORD:')
    for i in range(number_of_games):
        if conditions[i][1] == 'DRAW':
            print()
            print(record[i])
            game.grid = grids[i]
            game.display_grid()
            print(conditions[i])



