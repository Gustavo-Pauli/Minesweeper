import pygame, sys
import scripts.settings as settings
import scripts.menu as menu
import scripts.game as game


class Main:
    def __init__(self):
        self.screen = None  # set menu window size
        self.update_window_size(settings.START_WIDTH, settings.START_HEIGHT)
        self.game_state = self.GameState('Menu')
        self.clock = pygame.time.Clock()

        pygame.display.set_caption(settings.TITLE)  # set window title

        # global variables
        self.dt = 0

        # game states
        self.menu = menu.Menu(self)
        self.game = None
        # self.game = game.Game(self, settings.game.easy.ROWS, settings.game.easy.COLUMNS, settings.game.easy.BOMBS)


    def main_loop(self):
        # handle global events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # update delta time
        self.update_dt()

        # handle game states
        if self.game_state.list['Game']:
            self.game.update()
        if self.game_state.list['Menu']:
            self.menu.update()

        # print(self.clock.get_fps())  # print fps

        # update display (show things on screen)
        pygame.display.update()

    # calculate time between last clock tick (used for frame rate independence)
    def update_dt(self):
        self.dt = self.clock.tick(settings.MAX_FPS) / 1000

    def update_window_size(self, width, height, resizable=True):
        if resizable:
            self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        else:
            self.screen = pygame.display.set_mode((width, height))

    class GameState:
        def __init__(self, start_game_state: str):
            # list of possible game states
            self.list = {'Menu': False, 'Game': False}

            # raise error if invalid parameter is passed
            if start_game_state not in self.list:
                raise ValueError(start_game_state + ' is not a game state')

            # set the initial game state to True
            self.list[start_game_state] = True


if __name__ == '__main__':
    pygame.init()
    main = Main()
    while True:
        main.main_loop()
