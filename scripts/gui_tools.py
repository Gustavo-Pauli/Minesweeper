import pygame
import scripts.settings as settings
from scripts.vector2 import *


def text_renderer(screen_surface: pygame.surface, text: str, size: int, pos=(0, 0), align='center', color=settings.color.WHITE, font_path=settings.path.FONT_LIGHT_CONDENSED):
    font = pygame.font.Font(font_path, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()

    '''
    if align == 'center':
        text_rect.center = pos
    elif align == 'left':
        text_rect.bottomleft = pos
    elif align == 'right':
        text_rect.bottomright = pos
    else:
        raise ValueError('Align option not valid')
    '''

    if align == 'center':
        text_rect.center = pos
    elif align == 'top':
        text_rect.top = pos
    elif align == 'left':
        text_rect.left = pos
    elif align == 'bottom':
        text_rect.bottom = pos
    elif align == 'right':
        text_rect.right = pos
    elif align == 'topleft':
        text_rect.topleft = pos
    elif align == 'midleft':
        text_rect.midleft = pos
    elif align == 'bottomleft':
        text_rect.bottomleft = pos
    elif align == 'midbottom':
        text_rect.midbottom = pos
    elif align == 'bottomright':
        text_rect.bottomright = pos
    elif align == 'midright':
        text_rect.midright = pos
    elif align == 'topright':
        text_rect.topright = pos
    elif align == 'midtop':
        text_rect.midtop = pos
    else:
        raise ValueError("'" + align + "' is not a valid align option")

    screen_surface.blit(text_surface, text_rect)


def import_image(image_path: str, scale=1.0, alpha=False) -> pygame.surface:
    image_surface = None
    try:
        if alpha:
            image_surface = pygame.image.load(image_path).convert_alpha()
        else:
            image_surface = pygame.image.load(image_path).convert()
    except:
        raise ValueError('Invalid image file path')

    if scale != 1.0:
        image_surface = pygame.transform.smoothscale(image_surface, (int(image_surface.get_width() * scale), int(image_surface.get_height() * scale)))
    return image_surface


def grid_to_screen_pos(pos):
    return (settings.LEFT_MARGIN + pos[1] * settings.CELL_SIZE,
           settings.GRID_MARGIN[0] + settings.HUD_MARGIN[0] + settings.HUD_MARGIN[2] + settings.HUD_SIZE + pos[0] * settings.CELL_SIZE)


def screen_to_grid_pos(pos, rows, columns):
    grid_mouse_pos = (pos[0] - settings.LEFT_MARGIN, pos[1] - settings.HUD_MARGIN[0] - settings.HUD_MARGIN[2] - settings.HUD_SIZE - settings.GRID_MARGIN[0])

    # return if clicked out of grid
    if grid_mouse_pos[0] < 0 or grid_mouse_pos[1] < 0 \
            or grid_mouse_pos[0] >= settings.CELL_SIZE * columns \
            or grid_mouse_pos[1] >= settings.CELL_SIZE * rows:
        return None

    # calculate cordinates of cell clicked
    return grid_mouse_pos[1] // settings.CELL_SIZE, grid_mouse_pos[0] // settings.CELL_SIZE


# def V2ToInt(vector: pygame.Vector2):
#     return round(vector.x), round(vector.y)


# creates clickable buttons
class Button:
    def __init__(self, screen: pygame.surface, image: pygame.surface, pos=(0, 0), align='center', scale=1.0):
        self.screen = screen
        self.image = pygame.transform.smoothscale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))
        self.pos = pos
        self.rect = self.image.get_rect()
        self.align = align
        self.is_holding_click = False
        self.clicked_this_frame = False

        self.update_pos(pos)

    def render(self):
        self.screen.blit(self.image, self.rect)

    def check_collision(self):
        action = False
        mouse_pos = pygame.mouse.get_pos()

        # check if clicked
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed(3)[0] and not self.is_holding_click:
                self.is_holding_click = True
                action = True
        if not pygame.mouse.get_pressed(3)[0]:
            self.is_holding_click = False

        return action

    def update_pos(self, new_pos: [int, int]):
        self.pos = new_pos

        # alignment
        if self.align == 'center':
            self.rect.center = self.pos
        elif self.align == 'top':
            self.rect.top = self.pos
        elif self.align == 'left':
            self.rect.left = self.pos
        elif self.align == 'bottom':
            self.rect.bottom = self.pos
        elif self.align == 'right':
            self.rect.right = self.pos
        elif self.align == 'topleft':
            self.rect.topleft = self.pos
        elif self.align == 'midleft':
            self.rect.midleft = self.pos
        elif self.align == 'bottomleft':
            self.rect.bottomleft = self.pos
        elif self.align == 'midbottom':
            self.rect.midbottom = self.pos
        elif self.align == 'bottomright':
            self.rect.bottomright = self.pos
        elif self.align == 'midright':
            self.rect.midright = self.pos
        elif self.align == 'topright':
            self.rect.topright = self.pos
        elif self.align == 'midtop':
            self.rect.midtop = self.pos
        else:
            raise ValueError("'" + self.align + "' is not a valid align option")
