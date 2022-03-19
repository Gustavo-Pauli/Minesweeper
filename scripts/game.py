import pygame
import random
import time
import os.path
import json
import sys
from math import floor
import scripts.images
import scripts.settings as settings
import scripts.gui_tools as gui_tools
import scripts.menu as menu


class Game:
    def __init__(self, main, difficulty, custom_size=None):
        """

        :param main: Main class object instance
        :param difficulty: 0: easy, 1: medium, 2: hard, 3: custom
        :param custom_size: [int rows, int columns, int bombs]
        """
        self.main = main
        self.difficulty = difficulty
        self.custom_size = custom_size
        self.images = scripts.images.GameImages('blue')  # initialize images

        # determine how to start grid
        if difficulty != 3:
            self.grid = Grid(self.main, self, settings.game.DIFF_DICT[difficulty]['rows'],
                             settings.game.DIFF_DICT[difficulty]['columns'],
                             settings.game.DIFF_DICT[difficulty]['bombs'])
        else:
            self.grid = Grid(self.main, self, custom_size[0], custom_size[1], custom_size[2])

        self.update_window_size()  # change window size relative to current grid size
        self.ui = UI(self)

        self.clicked = True  # variable used to don't allow multiple clicks if holding mouse button

    def update(self):
        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.check_input()
        self.ui.update()

        # render
        self.main.screen.fill(settings.color.BACKGROUND)
        self.grid.render()
        self.ui.render()

    def update_window_size(self):
        # change window size accordingly to cells size
        self.main.update_window_size(
                settings.CELL_SIZE * self.grid.columns + settings.LEFT_MARGIN + settings.RIGHT_MARGIN,
                settings.CELL_SIZE * self.grid.rows + settings.GRID_MARGIN[0] + settings.GRID_MARGIN[2] +
                settings.HUD_MARGIN[0] + settings.HUD_MARGIN[2] + settings.HUD_SIZE)

    # ====== CHECK INPUTS

    # check all inputs
    def check_input(self):
        # ui input
        self.ui.check_input()

        # grid input
        left_clicked_cell = self.check_left_click()
        if left_clicked_cell is not None:
            self.left_click(left_clicked_cell)

        right_clicked_cell = self.check_right_click()
        if right_clicked_cell is not None:
            self.right_click(right_clicked_cell)

    def check_right_click(self) -> (int, int):
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

    def check_left_click(self) -> (int, int):
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
        if self.grid.block_input:
            return None

        clicked_cell = self.grid.cell_list[clicked_cell_pos[0]][clicked_cell_pos[1]]

        # don't do nothing if the clicked cell is flagged
        if clicked_cell.flagged:
            return

        # start game if is the first click
        if not self.grid.started:
            self.grid.start_game(clicked_cell_pos)
            self.grid.started = True

        # if clicked on a bomb
        if clicked_cell.type == -1:
            self.grid.lost_game(clicked_cell)

        # reveal
        clicked_cell.reveal()

    def right_click(self, clicked_cell):
        if self.grid.block_input:
            return None

        i = clicked_cell[0]
        j = clicked_cell[1]

        self.grid.cell_list[i][j].flag()

    # ====== SAVE / LOAD

    def save_game(self):
        # save if won and is the best time
        if not os.path.exists(settings.path.SAVE_FOLDER):
            os.makedirs(settings.path.SAVE_FOLDER)

        print(self.main.save)

        # save score
        if self.grid.won and self.main.game.difficulty != 3 and\
                (self.main.save['score'][str(self.main.game.difficulty)] == 'None' or
                 self.ui.timer.elapsed_time < self.main.save['score'][str(self.main.game.difficulty)]):
            self.main.save['score'][str(self.main.game.difficulty)] = floor(self.ui.timer.elapsed_time)

        with open(settings.path.SAVE, 'w', encoding='utf-8') as file:
            json.dump(self.main.save, file, ensure_ascii=False, indent=4)
            file.close()


# generate grid of cells until valid, verify if won
class Grid:
    def __init__(self, main, game, rows, columns, bombs):
        # raise error if passed wrong parameters
        if rows < 9:
            raise ValueError('rows cant be less than 9')
        if columns < 9:
            raise ValueError('columns cant be less than 9')
        if bombs < 1:
            raise ValueError('bombs cant be less than 1')
        if bombs > (rows * columns) - 9:
            raise ValueError('too many bombs')

        self.main = main
        self.game = game
        self.rows = rows
        self.columns = columns
        self.bombs = bombs

        self.size = int(rows * columns)
        self.revealed_cells = 0  # if this is equal to (self.size - self.bombs_num) the game end (winned)
        self.started = False
        self.won = False
        self.lost = False
        self.block_input = False  # if user can interact with the grid

        # create a list with empty cells to be filled later
        self.cell_list = self.create_cell_list(self.rows, self.columns)

        # DEBUG print number of rows and columns
        print('grid initialized with: ' + str(self.rows) + ' rows, ' + str(self.columns) + ' columns and ' + str(self.bombs) + ' bombs')

    # render all cells on screen
    def render(self):
        for i in range(self.rows):
            for j in range(self.columns):
                self.cell_list[i][j].render()
                # print('rendering (' + str(x) + ' ' + str(y) + ')')  # debug

    # start the game (generate bombs and numbers, start timer, etc)
    def start_game(self, first_clicked_cell):
        self.generate_bombs(first_clicked_cell)
        self.generate_numbers()
        self.main.game.ui.timer.start_timer()

    def lost_game(self, clicked_bomb_cell):
        # end game, stop game inputs, stop timer
        self.block_input = True
        self.lost = True
        self.main.game.ui.timer.end_timer()

        # reveal all bombs
        for i in range(self.rows):
            for j in range(self.columns):
                if self.cell_list[i][j].type == -1:  # if is a bomb
                    self.cell_list[i][j].reveal()

        # change clicked bomb to exploded image
        clicked_bomb_cell.exploded = True

    def won_game(self):
        self.won = True
        self.block_input = True
        self.main.game.ui.timer.end_timer()
        # print(self.main.game)
        self.main.game.save_game()

    # ====== START FUNCTIONS

    # create a 'empty' list of cells
    def create_cell_list(self, rows, columns):
        return [[Cell(self.main, 0, (x, y)) for y in range(columns)] for x in range(rows)]

    # generate bombs in random locations
    def generate_bombs(self, first_clicked_cell_pos):
        # get adjacents cells of clicked cell to dont spawn bomb on then
        adjacents_cells_pos = [cell.pos for cell in self.get_adjacent_cells(first_clicked_cell_pos) if
                               cell is not None]

        # generate all bombs
        bombs_generated = 0
        while bombs_generated < self.bombs:
            # generate a random cell location
            bomb_int_location = random.randint(0, self.size - 1)
            bomb_location = (bomb_int_location % self.rows, bomb_int_location // self.rows)
            bomb_cell = self.cell_list[bomb_location[0]][bomb_location[1]]

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
                if self.cell_list[i][j].type == -1:
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
                    self.cell_list[i][j].type = nearby_bombs

    # ====== ======

    # check if all non-bomb cells are open
    def check_if_won(self):
        if not self.lost and self.size - self.bombs == self.revealed_cells:
            self.won_game()

    def get_adjacent_cells(self, mid_cell_cord: (int, int)):
        i, j = mid_cell_cord  # mid cell location
        cells_list = [None] * 9

        # add all valid adjacents cells to cell_list
        for x in (-1, 0, 1):
            for y in (-1, 0, 1):
                if 0 <= i - x < self.rows and 0 <= j - y < self.columns:
                    cells_list[(x + 1) * 3 + (y + 1)] = self.cell_list[i - x][j - y]

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
                                and not self.main.game.grid.cell_list[self.pos[0] - x][self.pos[1] - y].type == -1:
                            self.main.game.grid.cell_list[self.pos[0] - x][self.pos[1] - y].reveal()

            # check if won
            self.main.game.grid.check_if_won()

    # put or remove the flag of the cell
    def flag(self):
        if self.flagged:
            self.flagged = False
        else:
            self.flagged = True


class UI:
    def __init__(self, game):
        self.main = game.main
        self.game = game

        self.margin = [settings.HUD_MARGIN[0], settings.RIGHT_MARGIN, settings.HUD_MARGIN[2], settings.LEFT_MARGIN]

        self.timer = self.Timer(self)

        self.menu_button = gui_tools.Button(self.main.screen, self.game.images.menu, (self.margin[3], self.margin[0]), 'topleft')
        self.restart_button = gui_tools.Button(self.main.screen, self.game.images.restart, (self.main.screen.get_width() - self.margin[1], self.margin[0]), 'topright')

    def update(self):
        self.timer.update()

    def render(self):
        self.menu_button.render()
        self.restart_button.render()
        self.timer.render()

        # if won or lost (Win/Lose screen)
        if self.main.game.grid.won:
            self.__render_won_screen()
        if self.main.game.grid.lost:
            self.__render_lost_screen()

    def check_input(self):
        if self.menu_button.check_collision() and not self.game.clicked:
            self.main.menu = menu.Menu(self.main)
            self.main.game_state.list['Menu'] = True
            self.main.game_state.list['Game'] = False

        if self.restart_button.check_collision() and not self.game.clicked:
            self.main.game = Game(self.main, self.game.difficulty, self.game.custom_size)

    def __render_lost_screen(self):
        # DEBUG
        gui_tools.text_renderer(self.main.screen, 'You Lost!', 64, (
            pygame.display.get_window_size()[0] // 2, pygame.display.get_window_size()[1] // 2))

    def __render_won_screen(self):
        # DEBUG
        gui_tools.text_renderer(self.main.screen, 'You Won!', 64, (
            pygame.display.get_window_size()[0] // 2, pygame.display.get_window_size()[1] // 2))

    # TODO passing game class instance leave room for errors, cause if instanced in wrong order the program may crash
    class Timer:
        def __init__(self, ui):
            self.main = ui.game.main
            self.ui = ui
            self.pos = (self.main.screen.get_width() // 2, self.ui.margin[0] + 4)
            self.started = False
            self.stopped = False
            self.start_time = 0
            self.elapsed_time = 0

        def update(self):
            if self.started and not self.stopped:
                # update elapsed time
                self.elapsed_time = time.monotonic() - self.start_time

            # time cap
            # if self.started and not self.stopped and self.elapsed_time > 3599:
            #     self.elapsed_time = 3599

        def render(self):
            gui_tools.text_renderer(self.main.screen, '%02d:%02d' % divmod(self.elapsed_time, 60), 21, self.pos, 'midtop', font_path=settings.path.FONT_REGULAR)

        def start_timer(self):
            self.started = True
            self.start_time = time.monotonic()

        def end_timer(self):
            self.stopped = True
