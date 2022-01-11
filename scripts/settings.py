# CONSTANTS
from dataclasses import dataclass

import pygame

# TODO maybe add @dataclass to separate settings into objects

# ========== SETTINGS ==========

# screen
# medium 444x504
START_WIDTH = 316
START_HEIGHT = 376
TITLE = 'Minesweeper'
MAX_FPS = 300

# sizes
CELL_SIZE = 32
HUD_SIZE = 24

HUD_MARGIN = (14, 14, 14, 14)  # top, right, bottom, left
GRID_MARGIN = (0, 14, 14, 14)  # top, right, bottom, left

LEFT_MARGIN = max(HUD_MARGIN[3], GRID_MARGIN[3])
RIGHT_MARGIN = max(HUD_MARGIN[1], GRID_MARGIN[1])


# audio

# ========== GAME ==========


@dataclass
class game:
    @dataclass
    class easy:
        ROWS = 9
        COLUMNS = 9
        BOMBS = 10

    @dataclass
    class medium:
        ROWS = 13
        COLUMNS = 13
        BOMBS = 25

    @dataclass
    class hard:
        ROWS = 16
        COLUMNS = 16
        BOMBS = 40


# ========== COLORS ==========


@dataclass
class color:
    WHITE = pygame.color.Color(255, 255, 255)

    BACKGROUND = pygame.color.Color(16, 28, 38)


# ========== FILES PATHS ==========


@dataclass
class path:
    # ====== FONTS
    FONT_LIGHT_CONDENSED = 'assets/fonts/Bahnschrift-LightCondensed.ttf'
    FONT_SEMIBOLD_CONDENSED = 'assets/fonts/Bahnschrift-BoldSemiCondensed.ttf'
    FONT_CONDENSED = 'assets/fonts/Bahnschrift-Condensed.ttf'
    FONT_REGULAR = 'assets/fonts/Bahnschrift-Regular.ttf'

    # ====== IMAGES
    # MENU
    PLAY_BUTTON = 'assets/art/menu/PlayButton.png'
    LEFT_ARROW = 'assets/art/menu/LeftArrow.png'
    RIGHT_ARROW = 'assets/art/menu/RightArrow.png'

    # GAME GRID
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

    # GAME UI
    MENU = 'assets/art/game/ui/MenuButton.png'
    RESTART = 'assets/art/game/ui/RestartButton.png'
