from collections import namedtuple

import pygame
import scripts.gui_tools as gui_tools
import scripts.settings as settings
import scripts.images as images
import main


class Menu:
    def __init__(self, main_instance: main.Main):
        self.main = main_instance

        self.screen_center = (self.main.screen.get_width() / 2, self.main.screen.get_height() / 2)

        self.images = images.MenuImages()  # initialize menu images

        self.menu_state = self.MenuState('MainMenu')
        self.main_menu = MainMenu(self.main, self)

    def update(self):
        self.screen_center = (self.main.screen.get_width() / 2, self.main.screen.get_height() / 2)

        # menu states
        if self.menu_state.list['MainMenu']:
            self.main_menu.update()

    class MenuState:
        def __init__(self, start_menu_state: str):
            # list of possible menu states
            self.list = {'MainMenu': False}

            # raise error if invalid parameter is passed
            if start_menu_state not in self.list:
                raise ValueError(start_menu_state + ' is not a menu state')

            # set the initial game state to True
            self.list[start_menu_state] = True


class MainMenu:
    def __init__(self, main_instance: main.Main, menu_instance: Menu):
        self.main = main_instance
        self.menu = menu_instance

        # button list class
        # self.ButtonList = namedtuple('ButtonList', ['play arrow_left arrow_right'])
        # self.button_list = None
        # self.button_dict = {}
        # self.initialize_buttons()
        self.play_button = gui_tools.Button(self.main.screen, self.menu.images.play, self.menu.screen_center)

    def update(self):
        # check buttons collisions

        # ====== DRAW

        # draw background
        self.main.screen.fill(settings.BACKGROUND_COLOR)

        self.play_button.update_pos(self.menu.screen_center)
        self.play_button.render()

        # draw buttons
        # for button in self.button_dict:
        #     button.draw()

    def initialize_buttons(self):
        menu_images = images.MenuImages()

        # self.button_dict = {
        #     'play': gui_tools.Button(self.main.screen, self.main.menu.images.play, self.main.menu.screen_center),
        # }



        # self.play_button_image = pygame.image.load(settings.PLAY_BUTTON_PATH).convert_alpha()
        # self.play_button = gui_tools.Button(self.main.screen, settings.PLAY_BUTTON_PATH, (settings.WIDTH, settings.HEIGHT))
