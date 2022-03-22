import sys

import pygame
import scripts.settings as settings


def text_renderer(screen_surface: pygame.surface, text: str, size: int, pos=(0, 0), align='center',
                  color=settings.color.WHITE, font_path=settings.path.FONT_LIGHT_CONDENSED):
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
        image_surface = pygame.transform.smoothscale(image_surface, (
        int(image_surface.get_width() * scale), int(image_surface.get_height() * scale)))
    return image_surface


def grid_to_screen_pos(pos):
    return (settings.LEFT_MARGIN + pos[1] * settings.CELL_SIZE,
            settings.GRID_MARGIN[0] + settings.HUD_MARGIN[0] + settings.HUD_MARGIN[2] + settings.HUD_SIZE + pos[
                0] * settings.CELL_SIZE)


def screen_to_grid_pos(pos, rows, columns):
    grid_mouse_pos = (pos[0] - settings.LEFT_MARGIN,
                      pos[1] - settings.HUD_MARGIN[0] - settings.HUD_MARGIN[2] - settings.HUD_SIZE -
                      settings.GRID_MARGIN[0])

    # return if clicked out of grid
    if grid_mouse_pos[0] < 0 or grid_mouse_pos[1] < 0 \
            or grid_mouse_pos[0] >= settings.CELL_SIZE * columns \
            or grid_mouse_pos[1] >= settings.CELL_SIZE * rows:
        return None

    # calculate cordinates of cell clicked
    return grid_mouse_pos[1] // settings.CELL_SIZE, grid_mouse_pos[0] // settings.CELL_SIZE


class Button:
    """Create a clickable button"""
    def __init__(self, screen: pygame.surface, image: pygame.surface, pos=(0, 0), align='center', scale=1.0):
        self.screen = screen
        self.image = pygame.transform.smoothscale(image,
                                                  (int(image.get_width() * scale), int(image.get_height() * scale)))
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


class InputBox:
    """Input field for number values"""
    def __init__(self, screen: pygame.surface, image: pygame.surface, selected_image: pygame.surface, pos=(0, 0), max_characters=19,
                 max_min=(sys.maxsize, 0), initial_value=10, scale=1.0, left_margin=12, font_path=settings.path.FONT_REGULAR, font_size=28):
        self.screen = screen
        self.max_characters = max_characters
        self.max_number = max_min[0]
        self.min_number = max_min[1]
        self.image = pygame.transform.smoothscale(image,
                                                  (int(image.get_width() * scale), int(image.get_height() * scale)))
        self.selected_image = pygame.transform.smoothscale(selected_image, (int(selected_image.get_width() * scale), int(selected_image.get_height() * scale)))
        self.scale = scale
        self.left_margin = left_margin
        self.font_path = font_path
        self.font_size = font_size

        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.font = pygame.font.Font(font_path, font_size)
        self.text = str(initial_value)
        self.selected = False

        self.is_holding_click = False
        self.possible_keys_events = [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6,
                                     pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_KP0, pygame.K_KP1, pygame.K_KP2,
                                     pygame.K_KP3, pygame.K_KP4, pygame.K_KP5, pygame.K_KP6, pygame.K_KP7, pygame.K_KP8,
                                     pygame.K_KP9]

    def check_collision(self):
        """Get if clicked to change self.selected"""
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed(3)[0] and not self.is_holding_click:
            self.selected = not self.selected
            self.is_holding_click = True
        if not self.rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed(3)[0] and not self.is_holding_click:
            self.selected = False
        if not pygame.mouse.get_pressed(3)[0]:
            self.is_holding_click = False

    def render(self):
        # box
        if self.selected:
            self.screen.blit(self.selected_image, self.rect)
        else:
            self.screen.blit(self.image, self.rect)

        # text
        text_renderer(self.screen, self.text, self.font_size, (self.rect.centerx, self.rect.centery + 1), 'center')

    def update(self):
        # change text to min/max number if out of range
        if not self.selected:
            try:
                if int(self.text) < self.min_number:
                    self.text = str(self.min_number)
                elif int(self.text) > self.max_number:
                    self.text = str(self.max_number)
            except ValueError:
                self.text = str(self.min_number)

    def force_update_input(self):
        """Force update input value to clamp to min and max value anytime"""
        try:
            if int(self.text) < self.min_number:
                self.text = str(self.min_number)
            elif int(self.text) > self.max_number:
                self.text = str(self.max_number)
        except ValueError:
            self.text = str(self.min_number)

    def input_event(self, event):
        """
        :param event: Keydown event
        """
        if self.selected:
            if event.unicode in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] and len(self.text) < self.max_characters:
                # print(event.unicode)
                self.text = self.text + event.unicode
            if event.key == pygame.K_BACKSPACE:
                # print('backspace')
                self.text = self.text[:-1]

    def set_max_number(self, new_max_number: int):
        self.max_number = new_max_number
