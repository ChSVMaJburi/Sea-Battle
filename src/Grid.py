import global_variable as glob
from drawer import Drawer


class Grid(Drawer):
    def __init__(self, tl, offset):
        """
        title(str): Имена игроков будут отображаться в верхней части его сетки
        offset (int): Где начинается сетка (в количестве блоков)
        """
        self.tl = tl
        self.offset = offset
        self.__add_nums_letters()
        self.__sign()
        Drawer.grid(self.offset)

    def __add_nums_letters(self) -> None:
        """
        Рисует цифры 1-10 по вертикали и добавляет буквы под горизонталью
        линии для обеих сеток
        """
        for i in range(glob.MAX_DIGIT):
            num_ver = glob.font.render(str(i + 1), True, glob.BL)
            letters_hor = glob.font.render(
                glob.LETTERS[i], True, glob.BL)
            num_ver_width = num_ver.get_width()
            num_ver_height = num_ver.get_height()
            letters_hor_width = letters_hor.get_width()

            glob.screen.blit(num_ver, (
                glob.l_margin - (glob.block_sz // 2 + num_ver_width // 2) + self.offset * glob.block_sz,
                glob.upp_margin + i * glob.block_sz + (glob.block_sz // 2 - num_ver_height // 2)))

            glob.screen.blit(letters_hor, (glob.l_margin + i * glob.block_sz + (glob.block_sz // 2 -
                                                                                letters_hor_width // 2) + self.offset * glob.block_sz,
                                           glob.upp_margin + glob.GRID_SIZE * glob.block_sz))

    def __sign(self) -> None:
        """
        Помещает имена игроков в центр над сетками
        """
        player = glob.font.render(self.tl, True, glob.RED)
        sign_width = player.get_width()
        glob.screen.blit(player, (glob.l_margin + 5 * glob.block_sz - sign_width // 2 +
                                  self.offset * glob.block_sz,
                                  glob.upp_margin - glob.block_sz // 2 - glob.font_sz))
