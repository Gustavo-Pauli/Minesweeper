import pygame, sys
import scripts.settings as settings
import scripts.menu as menu
import scripts.game as game


class Main:
    def __init__(self):
        # pygame.init()

        self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))  # set menu window size
        self.game_states = GameState('Game')
        self.clock = pygame.time.Clock()

        # game states
        self.menu = menu.MainMenu(self)
        self.game = game.Game(self, 9, 9, 10)

        # window
        pygame.display.set_caption(settings.TITLE)

        # global variables
        self.dt = 0

    def main_loop(self):
        # handle global events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # update delta time
        self.update_dt()

        # handle game states
        if self.game_states.list['Game']:
            self.game.update()
        if self.game_states.list['Menu']:
            # update menu
            pass

        # print(self.clock.get_fps())

        # update display (show things on screen)
        pygame.display.update()

    # calculate time between last clock tick (used for frame rate independence)
    def update_dt(self):
        self.dt = self.clock.tick(settings.MAX_FPS) / 1000


class GameState:
    def __init__(self, start_game_state):
        # game states list
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
