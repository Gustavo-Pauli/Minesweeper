import scripts.settings as settings
import scripts.gui_tools as gui_tools


class GameImages:
    def __init__(self, color='blue'):
        # TODO determine which COLOR to load

        self.cell_cover = gui_tools.import_image(settings.CELL_COVER_PATH, settings.CELL_SIZE / 128)
        self.cell_bomb = gui_tools.import_image(settings.CELL_BOMB_PATH, settings.CELL_SIZE / 128)
        self.cell_exploded_bomb = gui_tools.import_image(settings.CELL_EXPLODED_BOMB_PATH, settings.CELL_SIZE / 128)
        self.cell_flag = gui_tools.import_image(settings.CELL_FLAG_PATH, settings.CELL_SIZE / 128)
        self.cell_0 = gui_tools.import_image(settings.CELL_0_PATH, settings.CELL_SIZE / 128)
        self.cell_1 = gui_tools.import_image(settings.CELL_1_PATH, settings.CELL_SIZE / 128)
        self.cell_2 = gui_tools.import_image(settings.CELL_2_PATH, settings.CELL_SIZE / 128)
        self.cell_3 = gui_tools.import_image(settings.CELL_3_PATH, settings.CELL_SIZE / 128)
        self.cell_4 = gui_tools.import_image(settings.CELL_4_PATH, settings.CELL_SIZE / 128)
        self.cell_5 = gui_tools.import_image(settings.CELL_5_PATH, settings.CELL_SIZE / 128)
        self.cell_6 = gui_tools.import_image(settings.CELL_6_PATH, settings.CELL_SIZE / 128)
        self.cell_7 = gui_tools.import_image(settings.CELL_7_PATH, settings.CELL_SIZE / 128)
        self.cell_8 = gui_tools.import_image(settings.CELL_8_PATH, settings.CELL_SIZE / 128)

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
        pass



