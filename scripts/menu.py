from collections import namedtuple
import sys

import pygame
import scripts.gui_tools as gui_tools
import scripts.settings as settings
import scripts.images as images
import scripts.game as game
# import main


class Menu:
    def __init__(self):
        import main
        self.main = main.Main()
        # print('Menu: ' + str(self.main))

        self.main.update_window_size(348, 386)  # easy mode size
        self.screen_center = (self.main.screen.get_width() / 2, self.main.screen.get_height() / 2)

        self.images = images.MenuImages()  # initialize menu images

        self.menu_state = self.MenuState('MainMenu')
        self.main_menu = MainMenu(self)

    def update(self):
        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                for box in self.main_menu.input_boxes:
                    box.input_event(event)

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
    def __init__(self, menu_instance: Menu):
        import main
        self.main = main.Main()
        self.menu = menu_instance
        self.selected_difficulty = 0  # 0 = easy, 1 = medium, 2 = hard, 3 = custom

        self.columns_input_box = gui_tools.InputBox(self.main.screen, self.menu.images.input_box_2_digits,
                                                 self.menu.images.input_box_2_digits_selected,
                                                 (self.menu.screen_center[0] - 36, self.menu.screen_center[1]), 2,
                                                 (64, 9), 12)
        self.rows_input_box = gui_tools.InputBox(self.main.screen, self.menu.images.input_box_2_digits,
                                                    self.menu.images.input_box_2_digits_selected,
                                                    (self.menu.screen_center[0] + 36, self.menu.screen_center[1]),
                                                    2,
                                                    (36, 9), 12)
        self.bombs_input_box = gui_tools.InputBox(self.main.screen, self.menu.images.input_box_4_digits,
                                                  self.menu.images.input_box_4_digits_selected,
                                                  (self.menu.screen_center[0], self.menu.screen_center[1] + 40),
                                                  4,
                                                  (2295, 1), 9)
        self.input_boxes = [self.rows_input_box, self.columns_input_box, self.bombs_input_box]

        self.play_button = gui_tools.Button(self.main.screen, self.menu.images.play)
        self.left_arrow_button = gui_tools.Button(self.main.screen, self.menu.images.left_arrow)
        self.right_arrow_button = gui_tools.Button(self.main.screen, self.menu.images.right_arrow)
        self.buttons = [self.play_button, self.left_arrow_button, self.right_arrow_button]

    def update(self):
        # update buttons positions (for responsive UI)
        self.play_button.update_pos((self.menu.screen_center[0], self.main.screen.get_height() - 48))
        self.left_arrow_button.update_pos((26, self.menu.screen_center[1]))
        self.right_arrow_button.update_pos(((self.main.screen.get_width() - 26), self.menu.screen_center[1]))

        # ====== INPUT

        # detect buttons collision
        if self.play_button.check_collision():
            # Clamp input boxes to only the possible values for creating a Game
            self.rows_input_box.force_update_input()
            self.columns_input_box.force_update_input()
            self.bombs_input_box.set_max_number(int(self.columns_input_box.text) * int(self.rows_input_box.text) - 9)
            self.bombs_input_box.force_update_input()

            if self.selected_difficulty != 3:
                self.main.game = game.Game(self.selected_difficulty)
            else:
                self.main.game = game.Game(3, [int(self.rows_input_box.text), int(self.columns_input_box.text), int(self.bombs_input_box.text)])
            self.main.game_state.list['Menu'] = False
            self.main.game_state.list['Game'] = True

        if self.left_arrow_button.check_collision():
            if self.selected_difficulty != 0:
                self.selected_difficulty -= 1

        if self.right_arrow_button.check_collision():
            if self.selected_difficulty != 3:
                self.selected_difficulty += 1

        # input box
        if self.selected_difficulty == 3:
            for box in self.input_boxes:
                box.check_collision()
                box.update()

        # ====== ======

        self.render()

    def render(self):
        # render background
        self.main.screen.fill(settings.color.BACKGROUND)

        # render buttons
        self.play_button.render()
        if self.selected_difficulty != 0:
            self.left_arrow_button.render()
        if self.selected_difficulty != 3:
            self.right_arrow_button.render()

        # render selected difficulty
        if self.selected_difficulty == 0:
            gui_tools.text_renderer(self.main.screen, 'EASY', 42,
                                    (self.main.menu.screen_center[0], self.main.menu.screen_center[1] - 18),
                                    font_path=settings.path.FONT_SEMIBOLD_CONDENSED)
            gui_tools.text_renderer(self.main.screen, '9x9', 26,
                                    (self.main.menu.screen_center[0], self.main.menu.screen_center[1] + 18))
            if self.main.save['score']['0'] != 'None':
                gui_tools.text_renderer(self.main.screen, 'BEST %02d:%02d' % divmod(self.main.save['score']['0'], 60),
                                        15, (self.main.menu.screen_center[0], self.main.screen.get_height() - 76))
        elif self.selected_difficulty == 1:
            gui_tools.text_renderer(self.main.screen, 'MEDIUM', 42,
                                    (self.main.menu.screen_center[0], self.main.menu.screen_center[1] - 18),
                                    font_path=settings.path.FONT_SEMIBOLD_CONDENSED)
            gui_tools.text_renderer(self.main.screen, '12x12', 26,
                                    (self.main.menu.screen_center[0], self.main.menu.screen_center[1] + 18))
            if self.main.save['score']['1'] != 'None':
                gui_tools.text_renderer(self.main.screen, 'BEST %02d:%02d' % divmod(self.main.save['score']['1'], 60),
                                        15, (self.main.menu.screen_center[0], self.main.screen.get_height() - 76))
        elif self.selected_difficulty == 2:
            gui_tools.text_renderer(self.main.screen, 'HARD', 42,
                                    (self.main.menu.screen_center[0], self.main.menu.screen_center[1] - 18),
                                    font_path=settings.path.FONT_SEMIBOLD_CONDENSED)
            gui_tools.text_renderer(self.main.screen, '16x16', 26,
                                    (self.main.menu.screen_center[0], self.main.menu.screen_center[1] + 18))
            if self.main.save['score']['2'] != 'None':
                gui_tools.text_renderer(self.main.screen, 'BEST %02d:%02d' % divmod(self.main.save['score']['2'], 60),
                                        15, (self.main.menu.screen_center[0], self.main.screen.get_height() - 76))
        elif self.selected_difficulty == 3:
            gui_tools.text_renderer(self.main.screen, 'CUSTOM', 42,
                                    (self.main.menu.screen_center[0], self.main.menu.screen_center[1] - 39),
                                    font_path=settings.path.FONT_SEMIBOLD_CONDENSED)
            gui_tools.text_renderer(self.main.screen, 'x', 26,
                                    (self.main.menu.screen_center[0], self.main.menu.screen_center[1]))
            # input boxes
            for box in self.input_boxes:
                box.render()
