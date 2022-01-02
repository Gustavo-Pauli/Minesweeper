import pygame
import scripts.gui_tools as gui_tools
import scripts.settings as settings


class MainMenu:
    def __init__(self, main):
        self.main = main

        # self.play_button_image = pygame.image.load(settings.PLAY_BUTTON_PATH).convert_alpha()
        # self.play_button = gui_tools.Button(self.main.screen, settings.PLAY_BUTTON_PATH, (settings.WIDTH, settings.HEIGHT))
