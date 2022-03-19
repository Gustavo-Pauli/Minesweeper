import scripts.settings as settings
import scripts.gui_tools as gui_tools


class MainImages:
    def __init__(self):
        self.icon = gui_tools.import_image(settings.path.ICON, alpha=True)


class GameImages:
    def __init__(self, color='blue'):
        # TODO determine which COLOR to load

        # GRID
        self.cell_cover = gui_tools.import_image(settings.path.CELL_COVER, settings.CELL_SIZE / 128)
        self.cell_bomb = gui_tools.import_image(settings.path.CELL_BOMB, settings.CELL_SIZE / 128)
        self.cell_exploded_bomb = gui_tools.import_image(settings.path.CELL_EXPLODED_BOMB, settings.CELL_SIZE / 128)
        self.cell_flag = gui_tools.import_image(settings.path.CELL_FLAG, settings.CELL_SIZE / 128)
        self.cell_0 = gui_tools.import_image(settings.path.CELL_0, settings.CELL_SIZE / 128)
        self.cell_1 = gui_tools.import_image(settings.path.CELL_1, settings.CELL_SIZE / 128)
        self.cell_2 = gui_tools.import_image(settings.path.CELL_2, settings.CELL_SIZE / 128)
        self.cell_3 = gui_tools.import_image(settings.path.CELL_3, settings.CELL_SIZE / 128)
        self.cell_4 = gui_tools.import_image(settings.path.CELL_4, settings.CELL_SIZE / 128)
        self.cell_5 = gui_tools.import_image(settings.path.CELL_5, settings.CELL_SIZE / 128)
        self.cell_6 = gui_tools.import_image(settings.path.CELL_6, settings.CELL_SIZE / 128)
        self.cell_7 = gui_tools.import_image(settings.path.CELL_7, settings.CELL_SIZE / 128)
        self.cell_8 = gui_tools.import_image(settings.path.CELL_8, settings.CELL_SIZE / 128)

        # UI
        self.menu = gui_tools.import_image(settings.path.MENU, 0.375, True)
        self.restart = gui_tools.import_image(settings.path.RESTART, 0.375, True)

        # add bomb and num images to cell_dict
        self.cell_dict = {
            -1: self.cell_bomb,
            0: self.cell_0,
            1: self.cell_1,
            2: self.cell_2,
            3: self.cell_3,
            4: self.cell_4,
            5: self.cell_5,
            6: self.cell_6,
            7: self.cell_7,
            8: self.cell_8,
        }


class MenuImages:
    def __init__(self):
        self.play = gui_tools.import_image(settings.path.PLAY_BUTTON, alpha=True)
        self.left_arrow = gui_tools.import_image(settings.path.LEFT_ARROW, alpha=True)
        self.right_arrow = gui_tools.import_image(settings.path.RIGHT_ARROW, alpha=True)
        self.input_box_2_digits = gui_tools.import_image(settings.path.INPUT_BOX_2_DIGITS, alpha=True)
        self.input_box_2_digits_selected = gui_tools.import_image(settings.path.INPUT_BOX_2_DIGITS_SELECTED, alpha=True)
        self.input_box_4_digits = gui_tools.import_image(settings.path.INPUT_BOX_4_DIGITS, alpha=True)
        self.input_box_4_digits_selected = gui_tools.import_image(settings.path.INPUT_BOX_4_DIGITS_SELECTED, alpha=True)




