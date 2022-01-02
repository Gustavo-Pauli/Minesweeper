import pygame
import scripts.settings as settings


def text_renderer(screen_surface, text, align, size, pos, color):
    font = pygame.font.Font(settings.FONT_PATH, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()

    if align == 'center':
        text_rect.center = pos
    elif align == 'left':
        text_rect.bottomleft = pos
    elif align == 'right':
        text_rect.bottomright = pos
    else:
        raise ValueError('Align option not valid')

    screen_surface.blit(text_surface, text_rect)


def import_image(image_path, scale=1.0):
    image_surface = None
    try:
        image_surface = pygame.image.load(image_path).convert()
    except:
        raise ValueError('Invalid image file path')

    if scale != 1.0:
        image_surface = pygame.transform.smoothscale(image_surface, (int(image_surface.get_width() * scale), int(image_surface.get_height() * scale)))
    return image_surface


# creates clickables buttons
class Button:
    def __init__(self, screen, image, pos, scale=1.0):
        self.already_clicked = False
        self.screen = screen
        self.image = pygame.transform.smoothscale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (pos[0], pos[1])

    def render(self):
        pass

    def check_collision(self):
        pass
