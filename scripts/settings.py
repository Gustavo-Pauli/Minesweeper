# CONSTANTS

import pygame

# ========== SETTINGS ==========

# screen
WIDTH = 476
HEIGHT = 536
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

# fonts paths
FONT_PATH = 'assets/fonts/Roboto-Regular.ttf'

# images paths
PLAY_BUTTON_PATH = ''

CELL_COVER_PATH = 'assets/art/game/Cover.png'
CELL_FLAG_PATH = 'assets/art/game/Flag.png'
CELL_BOMB_PATH = 'assets/art/game/Bomb.png'
CELL_EXPLODED_BOMB_PATH = 'assets/art/game/BombExploded.png'
CELL_0_PATH = 'assets/art/game/0.png'
CELL_1_PATH = 'assets/art/game/1.png'
CELL_2_PATH = 'assets/art/game/2.png'
CELL_3_PATH = 'assets/art/game/3.png'
CELL_4_PATH = 'assets/art/game/4.png'
CELL_5_PATH = 'assets/art/game/5.png'
CELL_6_PATH = 'assets/art/game/6.png'
CELL_7_PATH = 'assets/art/game/7.png'
CELL_8_PATH = 'assets/art/game/8.png'


# sfx paths

