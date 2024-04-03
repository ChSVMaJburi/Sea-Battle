"""Реализован класс Grid наследуемый от Drawer. Цель нарисовать начальную сетку"""
import const_variable as const
from drawer import Drawer


class Grid(Drawer):
    """Класс для рисования начальных сеток"""
    def __init__(self, title: str, offset: int) -> None:
        """
        title(str): Имена игроков будут отображаться в верхней части его сетки
        offset (int): Где начинается сетка (в количестве блоков)
        """
        self.title = title
        self.offset = offset
        self.__add_nums_letters()
        self.__sign()
        Drawer.grid(self.offset)

    def __add_nums_letters(self) -> None:
        """
        Рисует цифры 1-10 по вертикали и добавляет буквы под горизонталью
        линии для обеих сеток
        """
        for digit in range(const.MAX_DIGIT):
            num_vertical = const.font.render(str(digit + 1), True, const.BLACK)
            letters_horizontal = const.font.render(
                const.LETTERS[digit], True, const.BLACK)
            num_vertical_width = num_vertical.get_width()
            num_vertical_height = num_vertical.get_height()
            letters_horizontal_width = letters_horizontal.get_width()

            const.screen.blit(num_vertical, (
                const.LEFT_MARGIN - (
                        const.BLOCK_SIZE // 2 + num_vertical_width // 2) +
                self.offset * const.BLOCK_SIZE,
                const.UP_MARGIN + digit * const.BLOCK_SIZE + (
                        const.BLOCK_SIZE // 2 - num_vertical_height // 2)))

            const.screen.blit(letters_horizontal,
                              (const.LEFT_MARGIN + digit * const.BLOCK_SIZE + (
                                      const.BLOCK_SIZE // 2 - letters_horizontal_width // 2) +
                               self.offset * const.BLOCK_SIZE,
                               const.UP_MARGIN + const.GRID_SIZE * const.BLOCK_SIZE))

    def __sign(self) -> None:
        """
        Помещает имена игроков в центр над сетками
        """
        player = const.font.render(self.title, True, const.RED)
        sign_width = player.get_width()
        const.screen.blit(player, (const.LEFT_MARGIN + 5 * const.BLOCK_SIZE - sign_width // 2 +
                                   self.offset * const.BLOCK_SIZE,
                                   const.UP_MARGIN - const.BLOCK_SIZE // 2 - const.FONT_SIZE))
