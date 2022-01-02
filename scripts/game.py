import pygame
import random
# import math
# import scripts.image_surfaces as image_surfaces
import scripts.settings as settings
import scripts.gui_tools as gui_tools


# gui, chronometer, finished etc
class Game:
    def __init__(self, main, rows, columns, bombs):
        self.main = main
        self.grid = Grid(self.main, rows, columns, bombs)

        # initialize images and add bomb and num images to cell_dict
        self.cell_dict = {}
        self.initialize_images()

        self.clicked = False  # variable used to don't allow multiple clicks if holding mouse button

    def update(self):
        self.check_input()

        # render
        self.main.screen.fill(settings.BACKGROUND_COLOR)
        self.grid.render()

        # DEBUG show text if won or losed
        if self.grid.won:
            gui_tools.text_renderer(self.main.screen, 'You Won!', 'center', 64, (pygame.display.get_window_size()[0]//2, pygame.display.get_window_size()[1]//2), settings.WHITE)
        if self.grid.lost:
            gui_tools.text_renderer(self.main.screen, 'You Lost!', 'center', 64, (pygame.display.get_window_size()[0] // 2, pygame.display.get_window_size()[1] // 2), settings.WHITE)

    def initialize_images(self):
        self.cell_cover_surface = gui_tools.import_image(settings.CELL_COVER_PATH, settings.CELL_SIZE / 128)
        self.cell_bomb_surface = gui_tools.import_image(settings.CELL_BOMB_PATH, settings.CELL_SIZE / 128)
        self.cell_exploded_bomb_surface = gui_tools.import_image(settings.CELL_EXPLODED_BOMB_PATH, settings.CELL_SIZE / 128)
        self.cell_flag_surface = gui_tools.import_image(settings.CELL_FLAG_PATH, settings.CELL_SIZE / 128)
        self.cell_0_surface = gui_tools.import_image(settings.CELL_0_PATH, settings.CELL_SIZE / 128)
        self.cell_1_surface = gui_tools.import_image(settings.CELL_1_PATH, settings.CELL_SIZE / 128)
        self.cell_2_surface = gui_tools.import_image(settings.CELL_2_PATH, settings.CELL_SIZE / 128)
        self.cell_3_surface = gui_tools.import_image(settings.CELL_3_PATH, settings.CELL_SIZE / 128)
        self.cell_4_surface = gui_tools.import_image(settings.CELL_4_PATH, settings.CELL_SIZE / 128)
        self.cell_5_surface = gui_tools.import_image(settings.CELL_5_PATH, settings.CELL_SIZE / 128)
        self.cell_6_surface = gui_tools.import_image(settings.CELL_6_PATH, settings.CELL_SIZE / 128)
        self.cell_7_surface = gui_tools.import_image(settings.CELL_7_PATH, settings.CELL_SIZE / 128)
        self.cell_8_surface = gui_tools.import_image(settings.CELL_8_PATH, settings.CELL_SIZE / 128)

        self.cell_dict = {
            -1: self.cell_bomb_surface,
            0: self.cell_0_surface,
            1: self.cell_1_surface,
            2: self.cell_2_surface,
            3: self.cell_3_surface,
            4: self.cell_4_surface,
            5: self.cell_5_surface,
            6: self.cell_6_surface,
            7: self.cell_7_surface,
            8: self.cell_8_surface,
        }

    # ====== CHECK INPUTS

    # check all inputs
    def check_input(self):
        left_clicked_cell = self.check_left_click()
        if left_clicked_cell is not None:
            self.left_click(left_clicked_cell)

        right_clicked_cell = self.check_right_click()
        if right_clicked_cell is not None:
            self.right_click(right_clicked_cell)

    def check_right_click(self):
        if self.grid.block_input:
            return None

        clicked_cell = None
        mouse_pos = pygame.mouse.get_pos()

        # find clicked cell
        if pygame.mouse.get_pressed(3)[2] and not self.clicked:
            self.clicked = True

            # mouse position inside the grid
            grid_mouse_pos = (mouse_pos[0] - settings.GRID_MARGIN[3], mouse_pos[1] - settings.GRID_MARGIN[0])

            # return if clicked out of grid
            if grid_mouse_pos[0] < 0 or grid_mouse_pos[1] < 0 or grid_mouse_pos[
                0] >= settings.CELL_SIZE * self.grid.columns or grid_mouse_pos[
                1] >= settings.CELL_SIZE * self.grid.rows:
                return None

            # calculate cell clicked
            clicked_cell = (grid_mouse_pos[1] // settings.CELL_SIZE, grid_mouse_pos[0] // settings.CELL_SIZE)
        if not pygame.mouse.get_pressed(3)[0] and not pygame.mouse.get_pressed(3)[2]:  # both mouse buttons
            self.clicked = False

        return clicked_cell

    def check_left_click(self):
        if self.grid.block_input:
            return None

        clicked_cell = None
        mouse_pos = pygame.mouse.get_pos()

        if pygame.mouse.get_pressed(3)[0] and not self.clicked:
            self.clicked = True

            # mouse position inside the grid
            grid_mouse_pos = (mouse_pos[0] - settings.GRID_MARGIN[3], mouse_pos[1] - settings.GRID_MARGIN[0])

            # return if clicked out of grid
            if grid_mouse_pos[0] < 0 or grid_mouse_pos[1] < 0 or grid_mouse_pos[0] >= settings.CELL_SIZE * self.grid.columns or grid_mouse_pos[1] >= settings.CELL_SIZE * self.grid.rows:
                return None

            # calculate cell clicked
            clicked_cell = (grid_mouse_pos[1] // settings.CELL_SIZE, grid_mouse_pos[0] // settings.CELL_SIZE)
        if not pygame.mouse.get_pressed(3)[0] and not pygame.mouse.get_pressed(3)[2]:  # both mouse buttons
            self.clicked = False

        return clicked_cell

    # ====== INPUT ACTIONS

    def left_click(self, clicked_cell):
        # start game if is the first click
        if not self.grid.started:
            self.grid.start_game(clicked_cell)
            self.grid.started = True

        # if clicked on a bomb TODO transfer this to a function
        if self.grid.list[clicked_cell[0]][clicked_cell[1]].type == -1:
            # end game, stop game inputs
            self.grid.block_input = True
            self.grid.lost = True

            # reveal all bombs
            for i in range(self.grid.rows):
                for j in range(self.grid.columns):
                    if self.grid.list[i][j].type == -1:  # if is a bomb
                        self.grid.list[i][j].reveal()

            # change clicked bomb to exploded image
            self.grid.list[clicked_cell[0]][clicked_cell[1]].exploded = True

        # reveal
        self.grid.list[clicked_cell[0]][clicked_cell[1]].reveal()

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

        # change window size accordingly to cells size
        self.main.screen = pygame.display.set_mode((settings.CELL_SIZE * self.columns + settings.GRID_MARGIN[1] + settings.GRID_MARGIN[3],
                                                    settings.CELL_SIZE * self.rows + settings.GRID_MARGIN[0] + settings.GRID_MARGIN[2]))

        # DEBUG print number of rows and columns
        print('grid initialized with: ' + str(self.rows) + ' rows and ' + str(self.columns) + ' columns')

    # render all cells on screen
    def render(self):
        for i in range(self.rows):
            for j in range(self.columns):
                self.list[i][j].render()
                # print('rendering (' + str(x) + ' ' + str(y) + ')')  # debug

    # ====== START

    # start the game (generate bombs and numbers, start timer, etc)
    def start_game(self, first_clicked_cell):
        self.generate_bombs(first_clicked_cell)
        self.generate_numbers()

    # generate bombs in random locations
    def generate_bombs(self, first_clicked_cell_pos):
        # raise error if has too much bombs
        if self.bombs_num >= self.size - 8:
            raise ValueError('too many bombs')

        adjacents_cells_pos = [cell.pos for cell in self.get_adjacents_cells(first_clicked_cell_pos)]

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

                adjacents = self.get_adjacents_cells((i, j))  # get adjacentes cells

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

    def get_adjacents_cells(self, mid_cell):
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
        self.pos = pos
        # print('creaing cell (' + str(pos[0]) + ' ' + str(pos[1]) + ')')  # debug
        self.revealed = False
        self.flagged = False
        self.exploded = False

    # render the cell on screen
    def render(self):
        # draw cover
        if not self.revealed and not self.flagged:
            self.main.screen.blit(self.main.game.cell_cover_surface,
                                  (settings.GRID_MARGIN[3] + self.pos[1] * settings.CELL_SIZE,
                                   settings.GRID_MARGIN[0] + self.pos[0] * settings.CELL_SIZE))

        # draw flag
        elif not self.revealed and self.flagged:
            # TODO change from cover to flag surface
            self.main.screen.blit(self.main.game.cell_flag_surface,
                                  (settings.GRID_MARGIN[3] + self.pos[1] * settings.CELL_SIZE,
                                   settings.GRID_MARGIN[0] + self.pos[0] * settings.CELL_SIZE))
        # draw exploded bomb
        elif self.exploded:
            # TODO change from cover to exploded surface
            self.main.screen.blit(self.main.game.cell_exploded_bomb_surface,
                                  (settings.GRID_MARGIN[3] + self.pos[1] * settings.CELL_SIZE,
                                   settings.GRID_MARGIN[0] + self.pos[0] * settings.CELL_SIZE))
        # draw revealed
        else:
            self.main.screen.blit(self.main.game.cell_dict[self.type],
                                  (settings.GRID_MARGIN[3] + self.pos[1] * settings.CELL_SIZE,
                                   settings.GRID_MARGIN[0] + self.pos[0] * settings.CELL_SIZE))
            # print('revealed cell ' + str(self.pos) + ' rendered')  # debug

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
                        if 0 <= self.pos[0]-x < self.main.game.grid.rows and 0 <= self.pos[1]-y < self.main.game.grid.columns and not self.main.game.grid.list[self.pos[0]-x][self.pos[1]-y].type == -1:
                            self.main.game.grid.list[self.pos[0]-x][self.pos[1]-y].reveal()


            # check if won
            self.main.game.grid.check_if_won()

    # put or remove the flag of the cell
    def flag(self):
        if self.flagged:
            self.flagged = False
        else:
            self.flagged = True
