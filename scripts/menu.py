from collections import namedtuple

import pygame
import scripts.gui_tools as gui_tools
import scripts.settings as settings
import scripts.images as images
import scripts.game as game
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
        self.selected_difficulty = 0  # 0 = easy, 1 = medium, 2 = hard, 3 = custom

        # TODO get save information
        self.best_time = {0: '00:37', 1: '01:52', 2: '05:11'}

        # WARNING TODO buttons are initializing at center, if change update_pos to event based, need to change here too
        self.play_button = gui_tools.Button(self.main.screen, self.menu.images.play)
        self.left_arrow_button = gui_tools.Button(self.main.screen, self.menu.images.left_arrow)
        self.right_arrow_button = gui_tools.Button(self.main.screen, self.menu.images.right_arrow)

    def update(self):
        # check buttons collisions

        # TODO try to change this update_pos to a event, called only when window is resized (window will not change size inside MENU)
        # update buttons positions (for responsive UI)
        self.play_button.update_pos((self.menu.screen_center[0], self.main.screen.get_height() - 48))
        self.left_arrow_button.update_pos((26, self.menu.screen_center[1]))
        self.right_arrow_button.update_pos(((self.main.screen.get_width() - 26), self.menu.screen_center[1]))

        # detect buttons collision
        if self.play_button.check_collision():
            if self.selected_difficulty == 0:
                self.main.game = game.Game(self.main, settings.game.easy.ROWS, settings.game.easy.COLUMNS, settings.game.easy.BOMBS)
            elif self.selected_difficulty == 1:
                self.main.game = game.Game(self.main, settings.game.medium.ROWS, settings.game.medium.COLUMNS, settings.game.medium.BOMBS)
            elif self.selected_difficulty == 2:
                self.main.game = game.Game(self.main, settings.game.hard.ROWS, settings.game.hard.COLUMNS, settings.game.hard.BOMBS)
            elif self.selected_difficulty == 3:
                self.main.game = game.Game(self.main, 16, 32, 30)
            self.main.game_state.list['Menu'] = False
            self.main.game_state.list['Game'] = True

        # ====== INPUT

        if self.left_arrow_button.check_collision():
            if self.selected_difficulty != 0:
                self.selected_difficulty -= 1

        if self.right_arrow_button.check_collision():
            if self.selected_difficulty != 3:
                self.selected_difficulty += 1

        # ====== RENDER

        # render background
        self.main.screen.fill(settings.color.BACKGROUND)

        # render buttons
        self.play_button.render()
        self.left_arrow_button.render()
        self.right_arrow_button.render()

        # draw selected difficulty with size
        if self.selected_difficulty == 0:
            gui_tools.text_renderer(self.main.screen, 'EASY', 42, (self.main.menu.screen_center[0], self.main.menu.screen_center[1] - 18), font_path=settings.path.FONT_SEMIBOLD_CONDENSED)
            gui_tools.text_renderer(self.main.screen, '9x9', 26, (self.main.menu.screen_center[0], self.main.menu.screen_center[1] + 18))
            gui_tools.text_renderer(self.main.screen, 'BEST %s' % self.best_time[0], 15, (self.main.menu.screen_center[0], self.main.screen.get_height() - 76))
        elif self.selected_difficulty == 1:
            gui_tools.text_renderer(self.main.screen, 'MEDIUM', 42, (self.main.menu.screen_center[0], self.main.menu.screen_center[1] - 18), font_path=settings.path.FONT_SEMIBOLD_CONDENSED)
            gui_tools.text_renderer(self.main.screen, '12x12', 26, (self.main.menu.screen_center[0], self.main.menu.screen_center[1] + 18))
            gui_tools.text_renderer(self.main.screen, 'BEST %s' % self.best_time[1], 15, (self.main.menu.screen_center[0], self.main.screen.get_height() - 76))
        elif self.selected_difficulty == 2:
            gui_tools.text_renderer(self.main.screen, 'HARD', 42, (self.main.menu.screen_center[0], self.main.menu.screen_center[1] - 18), font_path=settings.path.FONT_SEMIBOLD_CONDENSED)
            gui_tools.text_renderer(self.main.screen, '16x16', 26, (self.main.menu.screen_center[0], self.main.menu.screen_center[1] + 18))
            gui_tools.text_renderer(self.main.screen, 'BEST %s' % self.best_time[2], 15, (self.main.menu.screen_center[0], self.main.screen.get_height() - 76))
        elif self.selected_difficulty == 3:
            gui_tools.text_renderer(self.main.screen, 'CUSTOM', 42, (self.main.menu.screen_center[0], self.main.menu.screen_center[1] - 18), font_path=settings.path.FONT_SEMIBOLD_CONDENSED)
            gui_tools.text_renderer(self.main.screen, '00x00', 26, (self.main.menu.screen_center[0], self.main.menu.screen_center[1] + 18))

        # TODO draw best time in selected difficulty




