import global_variable as variables
from draw import draw


class Grid(draw):
    def __init__(self, tl, offset):
        """
        title(str): Имена игроков будут отображаться в верхней части его сетки
        offset (int): Где начинается сетка (в количестве блоков)
        """
        self.tl = tl
        self.offset = offset
        self.__add_nums_letters()
        self.__sign()
        draw.grid(self.offset)

    def __add_nums_letters(self) -> None:
        """
        Рисует цифры 1-10 по вертикали и добавляет буквы под горизонталью
        линии для обеих сеток
        """
        for i in range(10):
            num_ver = variables.font.render(str(i + 1), True, variables.BL)
            letters_hor = variables.font.render(
                variables.LETTERS[i], True, variables.BL)
            num_ver_width = num_ver.get_width()
            num_ver_height = num_ver.get_height()
            letters_hor_width = letters_hor.get_width()

            variables.screen.blit(num_ver, (
                variables.l_margin - (variables.block_sz // 2 + num_ver_width // 2) + self.offset * variables.block_sz,
                variables.upp_margin + i * variables.block_sz + (variables.block_sz // 2 - num_ver_height // 2)))

            variables.screen.blit(letters_hor, (variables.l_margin + i * variables.block_sz + (variables.block_sz // 2 -
                                                                                               letters_hor_width // 2) + self.offset * variables.block_sz,
                                                variables.upp_margin + 10 * variables.block_sz))

    def __sign(self) -> None:
        """
        Помещает имена игроков в центр над сетками
        """
        player = variables.font.render(self.tl, True, variables.RED)
        sign_width = player.get_width()
        variables.screen.blit(player, (variables.l_margin + 5 * variables.block_sz - sign_width // 2 +
                                       self.offset * variables.block_sz,
                                       variables.upp_margin - variables.block_sz // 2 - variables.font_sz))
