import json
import os.path
import pygame
import sys
import threading
import scripts.menu as menu
import scripts.settings as settings
import scripts.images as images


class Main:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(Main, cls).__new__(cls)
            cls.__instance.__initialized = False
        return cls.__instance

    def __init__(self):
        if self.__initialized: return
        self.__initialized = True

        self.screen = None  # set menu window size
        self.game_state = self.GameState('Menu')
        self.clock = pygame.time.Clock()
        self.update_window_size(settings.START_WIDTH, settings.START_HEIGHT)
        self.main_images = images.MainImages()

        pygame.display.set_icon(self.main_images.icon)
        pygame.display.set_caption(settings.TITLE)  # set window title

        # global variables
        self.dt = 0

        # game states
        self.menu = menu.Menu()
        self.game = None

        self.save = {}  # all attributes in save json file
        self.load_save()

    def main_loop(self):
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

    def update_window_size(self, width, height, resizable=False):
        # print('width: ' + str(width) + ', height: ' + str(height))
        if resizable:
            self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        else:
            self.screen = pygame.display.set_mode((width, height))

    def load_save(self):
        if not os.path.exists(settings.path.SAVE_FOLDER):
            os.makedirs(settings.path.SAVE_FOLDER)

        try:
            with open(settings.path.SAVE, 'r', encoding='utf-8') as file:
                self.save = json.load(file)
                file.close()
        except (IOError, json.decoder.JSONDecodeError):
            with open(settings.path.SAVE, 'w', encoding='utf-8') as file:
                # create base save dictionary
                self.save['score'] = {'0': 'None', '1': 'None', '2': 'None'}
                file.close()

    class GameState:
        def __init__(self, start_game_state: str):
            # list of possible game states
            self.list = {'Menu': False, 'Game': False}

            # raise error if invalid parameter is passed
            if start_game_state not in self.list:
                raise ValueError(start_game_state + ' is not a game state')

            # set the initial game state to True
            self.list[start_game_state] = True


sys.setrecursionlimit(10000)
pygame.init()
main = Main()
# print('Main: ' + str(main))
while True:
    main.main_loop()
