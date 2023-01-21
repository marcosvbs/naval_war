import random
import game_rules

class Player:
    
    def __init__(self):
        self.bombs = game_rules.NUMBER_OF_BOMBS
        self.board = Board()

    def drop_bomb(self, game_controller_board, target_cell_row, target_cell_column):

            if self.check_if_cell_has_ship(game_controller_board, target_cell_row, target_cell_column):
                self.board.cells[target_cell_row][target_cell_column] = 'X'
                
            else:
                self.board.cells[target_cell_row][target_cell_column] = 'O'

    def check_if_cell_has_ship(self, game_controller_board, cell_row, cell_column):
        
        if game_controller_board.cells[cell_row][cell_column] == '#':
            return True
        else:
            return False           

class Board:

    def __init__(self):
        self.rows = game_rules.NUMBER_OF_BOARD_ROWS
        self.columns = game_rules.NUMBER_OF_BOARD_COLUMNS
        self.cells = self.create_cells(self.rows, self.columns)
        self.rows_labels = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
        self.columns_labels = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    def create_cells(self, rows, columns): 
        cells = []

        for row in range(rows):
            cells.append([])

            for column in range(columns):
                cells[row].append(' ')

        return cells

    def show_cells(self):

        print('')
        print('   ', end='')

        for column in range(self.columns):
            print(self.columns_labels[column], end=' ')

        print('')

        for row in range(self.rows):
            print(self.rows_labels[row], end=' ')

            for column in range(self.columns):
                print(f'|{self.cells[row][column]}', end='')
                
            print('|', end='\n')

        print('')

class Ship:

    def __init__(self, size, direction):
        self.size = size
        self.direction = direction
        self.location = []
        self.is_sunk = False

class GameController:

    def __init__(self):

        self.board = Board()
        self.ships = self.create_ships()

    def create_ships(self):

        ships = []

        for ship in range(game_rules.NUMBER_OF_SHIPS):
            new_ship = Ship(self.generate_ship_size(game_rules.MIN_SHIP_SIZE, game_rules.MAX_SHIP_SIZE), self.generate_ship_direction())
            ships.append(new_ship)

        return ships

    def generate_ship_size(self, minimum_size, maximum_size):

        ship_size = random.randint(minimum_size, maximum_size)

        return ship_size

    def generate_ship_direction(self):
        ship_direction = random.randint(0, 1)

        if ship_direction == 0:
            return 'horizontal'
        else:
            return 'vertical'
   
    def place_ships_on_board(self):

        for ship in self.ships:

            if ship.direction == 'horizontal':

                is_available = False

                while not is_available:
                    initial_cell_row = random.randint(0, self.board.rows - 1)
                    initial_cell_column = random.randint(0, (self.board.columns - 1) - ship.size)
                    
                    is_available = self.check_cell_availability(ship, initial_cell_row, initial_cell_column)

                for part in range(ship.size):
                    ship.location.append([initial_cell_column + part, initial_cell_row])
                    self.board.cells[initial_cell_column + part][initial_cell_row] = '#'

            else:
                is_available = False

                while not is_available:
                    initial_cell_row = random.randint(0, (self.board.rows - 1) - ship.size)
                    initial_cell_column = random.randint(0, self.board.columns - 1)
                    
                    is_available = self.check_cell_availability(ship, initial_cell_row, initial_cell_column)

                for part in range(ship.size):
                    ship.location.append([initial_cell_column, initial_cell_row  + part])
                    self.board.cells[initial_cell_column][initial_cell_row  + part] = '#'

    def check_cell_availability(self, ship, initial_cell_row, initial_cell_column):

        for cell in range(ship.size):

            if ship.direction == 'horizontal':
                if self.board.cells[initial_cell_column + cell][initial_cell_row] != ' ':
                    return False

            else:
                if self.board.cells[initial_cell_column][initial_cell_row + cell] != ' ':
                    return False

        return True   

    def get_target_cell_column(self):

        while True:

            try:
                column = -100
                while (column < self.board.columns_labels[0]) or (column > len(self.board.columns_labels)):
                    column = int(input("Escolha uma coluna: "))

                    if (column < self.board.columns_labels[0]) or (column > len(self.board.columns_labels)):
                        print("Por favor, escolha uma coluna valida...")

                column -= 1

                return column

            except ValueError:
                print("Por favor, escolha uma coluna valida...")

    def get_target_cell_row(self):

          while True:

            try:

                is_valid = False
                row = -1
                while not is_valid:
                    row = input("Escolha uma linha: ")
                    row_index = int(self.board.rows_labels.index(row))

                    if row_index == -1:
                        print("Por favor, escolha uma linha valida...")
                    else:

                        is_valid = True

                return row_index

            except ValueError:
                print("Por favor, escolha uma linha valida...")

    def check_sunk_ships(self, player_board):

        for ship in self.ships:

            for cell in ship.location:

                if player_board.cells[cell[0]][cell[1]] == 'X':
                    ship.is_sunk = True
                else:
                    ship.is_sunk = False
                    break

    def check_if_player_wins(self, player_board):

        for ship in self.ships:

            if ship.is_sunk == False:
                return False
            
        return True

    def check_ships_left(self):

        ships_left = 0

        for ship in self.ships:
            if not ship.is_sunk:
                ships_left +=1

        return ships_left