import pygame
import random
# from collections import namedtuple
# from main import *
# import main as main
import scripts.images
import scripts.settings as settings
import scripts.gui_tools as gui_tools
# from scripts.vector2 import *


# gui, chronometer, finished etc
class Game:
    def __init__(self, main, rows, columns, bombs):
        self.main = main
        self.images = scripts.images.GameImages('blue')  # initialize images
        self.grid = Grid(self.main, rows, columns, bombs)

        self.update_window_size()  # change window size relative to current grid size

        self.clicked = False  # variable used to don't allow multiple clicks if holding mouse button

    def update(self):
        self.check_input()

        # render
        self.main.screen.fill(settings.BACKGROUND_COLOR)
        self.grid.render()

        # DEBUG show text if won or losed
        if self.grid.won:
            gui_tools.text_renderer(self.main.screen, 'You Won!', 'center', 64, (
                pygame.display.get_window_size()[0] // 2, pygame.display.get_window_size()[1] // 2), settings.WHITE)
        if self.grid.lost:
            gui_tools.text_renderer(self.main.screen, 'You Lost!', 'center', 64, (
                pygame.display.get_window_size()[0] // 2, pygame.display.get_window_size()[1] // 2), settings.WHITE)

    def update_window_size(self):
        # change window size accordingly to cells size
        self.main.update_window_size(
                settings.CELL_SIZE * self.grid.columns + settings.LEFT_MARGIN + settings.RIGHT_MARGIN,
                settings.CELL_SIZE * self.grid.rows + settings.GRID_MARGIN[0] + settings.GRID_MARGIN[2] +
                settings.HUD_MARGIN[0] + settings.HUD_MARGIN[2] + settings.HUD_SIZE)

    # ====== CHECK INPUTS

    # check all inputs
    def check_input(self):
        left_clicked_cell = self.check_left_click()
        if left_clicked_cell is not None:
            self.left_click(left_clicked_cell)

        right_clicked_cell = self.check_right_click()
        if right_clicked_cell is not None:
            self.right_click(right_clicked_cell)

    def check_right_click(self) -> (int, int):
        if self.grid.block_input:
            return None

        clicked_cell_coordinates = None
        mouse_pos = pygame.mouse.get_pos()

        # find clicked cell
        if pygame.mouse.get_pressed(3)[2] and not self.clicked:
            self.clicked = True

            grid_cord = gui_tools.screen_to_grid_pos(mouse_pos, self.grid.rows, self.grid.columns)
            if grid_cord is not None:
                clicked_cell_coordinates = grid_cord

        if not pygame.mouse.get_pressed(3)[0] and not pygame.mouse.get_pressed(3)[2]:  # both mouse buttons
            self.clicked = False

        return clicked_cell_coordinates

    def check_left_click(self):
        if self.grid.block_input:
            return None

        clicked_cell = None
        mouse_pos = pygame.mouse.get_pos()

        if pygame.mouse.get_pressed(3)[0] and not self.clicked:
            self.clicked = True

            grid_pos = gui_tools.screen_to_grid_pos(mouse_pos, self.grid.rows, self.grid.columns)
            if grid_pos is not None:
                clicked_cell = grid_pos

        if not pygame.mouse.get_pressed(3)[0] and not pygame.mouse.get_pressed(3)[2]:  # both mouse buttons
            self.clicked = False

        return clicked_cell

    # ====== INPUT ACTIONS

    def left_click(self, clicked_cell_pos):
        clicked_cell = self.grid.list[clicked_cell_pos[0]][clicked_cell_pos[1]]

        # don't do nothing if the clicked cell is flagged
        if clicked_cell.flagged:
            return

        # start game if is the first click
        if not self.grid.started:
            self.grid.start_game(clicked_cell_pos)
            self.grid.started = True

        # if clicked on a bomb TODO transfer this to a function
        if clicked_cell.type == -1:
            # end game, stop game inputs
            self.grid.block_input = True
            self.grid.lost = True

            # reveal all bombs
            for i in range(self.grid.rows):
                for j in range(self.grid.columns):
                    if self.grid.list[i][j].type == -1:  # if is a bomb
                        self.grid.list[i][j].reveal()

            # change clicked bomb to exploded image
            clicked_cell.exploded = True

        # reveal
        clicked_cell.reveal()

    def right_click(self, clicked_cell):
        i = clicked_cell[0]
        j = clicked_cell[1]

        self.grid.list[i][j].flag()


# generate grid of cells until valid, verify if won
class Grid:
    def __init__(self, main, rows, columns, bombs):
        self.main = main
        self.rows = rows
        self.columns = columns

        self.bombs_num = bombs
        self.size = int(rows * columns)
        self.revealed_cells = 0  # if this is equal to (self.size - self.bombs_num) the game end (winned)
        self.timer = 0  # TODO implement this
        self.started = False
        self.won = False
        self.lost = False
        self.block_input = False  # if user can interact with the grid

        # TODO check if has minimun rows and columns

        # create a list with empty cells to be filled later
        self.list = self.create_cell_list(self.rows, self.columns)

        # DEBUG print number of rows and columns
        print('grid initialized with: ' + str(self.rows) + ' rows and ' + str(self.columns) + ' columns')

    # render all cells on screen
    def render(self):
        for i in range(self.rows):
            for j in range(self.columns):
                self.list[i][j].render()
                # print('rendering (' + str(x) + ' ' + str(y) + ')')  # debug

    # ====== START FUNCTIONS

    # start the game (generate bombs and numbers, start timer, etc)
    def start_game(self, first_clicked_cell):
        self.generate_bombs(first_clicked_cell)
        self.generate_numbers()

    # generate bombs in random locations
    def generate_bombs(self, first_clicked_cell_pos):
        # raise error if has too much bombs
        if self.bombs_num >= self.size - 8:
            raise ValueError('too many bombs')

        # get adjacents cells of clicked cell to dont spawn bomb on then
        adjacents_cells_pos = [cell.pos for cell in self.get_adjacent_cells(first_clicked_cell_pos) if
                               cell is not None]

        # generate all bombs
        bombs_generated = 0
        while bombs_generated < self.bombs_num:
            # generate a random cell location
            bomb_int_location = random.randint(0, self.size - 1)
            bomb_location = (bomb_int_location % self.rows, bomb_int_location // self.rows)
            bomb_cell = self.list[bomb_location[0]][bomb_location[1]]

            # if cell is not a bomb and not around first clicked cell, put a bomb. if is a bomb or first cell, generate again.
            if bomb_cell.type != -1 and bomb_cell.pos not in adjacents_cells_pos:
                bomb_cell.type = -1
                bombs_generated += 1
            else:
                continue

    # generate numbers around bombs
    def generate_numbers(self):
        for i in range(self.rows):
            for j in range(self.columns):
                # skip if is a bomb
                if self.list[i][j].type == -1:
                    continue

                # check how many bombs are nearby
                # nearby_bombs = 0
                # for x in (-1, 0, 1):
                #     for y in (-1, 0, 1):
                #         if 0 <= i-x < self.rows and 0 <= j-y < self.columns and self.list[i-x][j-y].type == -1:
                #             nearby_bombs += 1

                adjacents = self.get_adjacent_cells((i, j))  # get adjacentes cells

                # check how many bombs are nearby
                nearby_bombs = 0
                for cell in adjacents:
                    if cell is not None and cell.type == -1:
                        nearby_bombs += 1

                # change cell type if has bomb nearby
                if nearby_bombs > 0:
                    self.list[i][j].type = nearby_bombs

    # create a 'empty' list of cells
    def create_cell_list(self, rows, columns):
        return [[Cell(self.main, 0, (x, y)) for y in range(columns)] for x in range(rows)]

    # ====== ======

    # check if all non-bomb cells are open
    def check_if_won(self):
        if not self.lost and self.size - self.bombs_num == self.revealed_cells:
            self.won = True
            self.block_input = True

    def get_adjacent_cells(self, mid_cell):
        i, j = mid_cell  # mid cell location

        cells_list = [None] * 9

        # add all valid adjacents cells to cell_list
        for x in (-1, 0, 1):
            for y in (-1, 0, 1):
                if 0 <= i - x < self.rows and 0 <= j - y < self.columns:
                    cells_list[(x + 1) * 3 + (y + 1)] = self.list[i - x][j - y]

        return cells_list


class Cell:
    def __init__(self, main, cell_type, pos):
        # raise exception if cell_type is not valid
        if cell_type not in [-1, 0, 1, 2, 3, 4, 5, 6, 7, 8]:
            raise ValueError(cell_type + ' is not a valid cell type')

        self.main = main
        self.type = cell_type
        self.pos = pos  # coordinates in the grid
        # print('creating cell (' + str(pos[0]) + ' ' + str(pos[1]) + ')')  # debug
        self.revealed = False
        self.flagged = False
        self.exploded = False

    # render the cell on screen
    def render(self):
        # draw cover
        if not self.revealed and not self.flagged:
            self.main.screen.blit(self.main.game.images.cell_cover, gui_tools.grid_to_screen_pos(self.pos))
        # draw flag
        elif not self.revealed and self.flagged:
            self.main.screen.blit(self.main.game.images.cell_flag, gui_tools.grid_to_screen_pos(self.pos))
        # draw exploded bomb
        elif self.exploded:
            self.main.screen.blit(self.main.game.images.cell_exploded_bomb, gui_tools.grid_to_screen_pos(self.pos))
        # draw revealed
        else:
            self.main.screen.blit(self.main.game.images.cell_dict[self.type], gui_tools.grid_to_screen_pos(self.pos))

    # reveal the cell
    def reveal(self):
        if not self.revealed:
            self.revealed = True
            self.main.game.grid.revealed_cells += 1
            print('cell ' + str(self.pos) + ' revealed')

            # search around for other zeroes
            if self.type == 0:
                for x in (-1, 0, 1):
                    for y in (-1, 0, 1):
                        if 0 <= self.pos[0] - x < self.main.game.grid.rows\
                                and 0 <= self.pos[1] - y < self.main.game.grid.columns\
                                and not self.main.game.grid.list[self.pos[0] - x][self.pos[1] - y].type == -1:
                            self.main.game.grid.list[self.pos[0] - x][self.pos[1] - y].reveal()

            # check if won
            self.main.game.grid.check_if_won()

    # put or remove the flag of the cell
    def flag(self):
        if self.flagged:
            self.flagged = False
        else:
            self.flagged = True
