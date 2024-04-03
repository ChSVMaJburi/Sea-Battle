import global_variable as my_space
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
        for i in range(my_space.MAX_DIGIT):
            num_ver = my_space.font.render(str(i + 1), True, my_space.BL)
            letters_hor = my_space.font.render(
                my_space.LETTERS[i], True, my_space.BL)
            num_ver_width = num_ver.get_width()
            num_ver_height = num_ver.get_height()
            letters_hor_width = letters_hor.get_width()

            my_space.screen.blit(num_ver, (
                my_space.l_margin - (my_space.block_sz // 2 + num_ver_width // 2) + self.offset * my_space.block_sz,
                my_space.upp_margin + i * my_space.block_sz + (my_space.block_sz // 2 - num_ver_height // 2)))

            my_space.screen.blit(letters_hor, (my_space.l_margin + i * my_space.block_sz + (my_space.block_sz // 2 -
                                                                                letters_hor_width // 2) + self.offset * my_space.block_sz,
                                           my_space.upp_margin + my_space.GRID_SIZE * my_space.block_sz))

    def __sign(self) -> None:
        """
        Помещает имена игроков в центр над сетками
        """
        player = my_space.font.render(self.tl, True, my_space.RED)
        sign_width = player.get_width()
        my_space.screen.blit(player, (my_space.l_margin + 5 * my_space.block_sz - sign_width // 2 +
                                  self.offset * my_space.block_sz,
                                  my_space.upp_margin - my_space.block_sz // 2 - my_space.font_sz))
