# CONSTANTS
from dataclasses import dataclass

import pygame

# TODO maybe add @dataclass to separate settings into objects

# ========== SETTINGS ==========

# screen
START_WIDTH = 476
START_HEIGHT = 536
TITLE = 'Minesweeper'
MAX_FPS = 300

# sizes
CELL_SIZE = 32
HUD_SIZE = 32

HUD_MARGIN = (14, 14, 14, 14)
GRID_MARGIN = (14, 14, 14, 14)  # top, right, bottom, left

LEFT_MARGIN = max(HUD_MARGIN[3], GRID_MARGIN[3])
RIGHT_MARGIN = max(HUD_MARGIN[1], GRID_MARGIN[1])


# audio

# game

# ========== COLORS ==========

WHITE = pygame.color.Color(255, 255, 255)

BACKGROUND_COLOR = pygame.color.Color(16, 28, 38)

# ========== FILES PATHS ==========

@dataclass
class path:
    # ====== FONTS
    FONT = 'assets/fonts/Roboto-Regular.ttf'

    # ====== IMAGES
    # MENU
    PLAY_BUTTON = 'assets/art/menu/PlayButton.png'

    # GAME
    CELL_COVER = 'assets/art/game/Cover.png'
    CELL_FLAG = 'assets/art/game/Flag.png'
    CELL_BOMB = 'assets/art/game/Bomb.png'
    CELL_EXPLODED_BOMB = 'assets/art/game/BombExploded.png'
    CELL_0 = 'assets/art/game/0.png'
    CELL_1 = 'assets/art/game/1.png'
    CELL_2 = 'assets/art/game/2.png'
    CELL_3 = 'assets/art/game/3.png'
    CELL_4 = 'assets/art/game/4.png'
    CELL_5 = 'assets/art/game/5.png'
    CELL_6 = 'assets/art/game/6.png'
    CELL_7 = 'assets/art/game/7.png'
    CELL_8 = 'assets/art/game/8.png'
