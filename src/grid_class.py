"""Реализован класс Grid наследуемый от Drawer. Цель нарисовать начальную сетку"""
import global_variables as my_space
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
        self.__draw_grid()
        self.__add_nums_letters()
        self.__sign()

    def __draw_grid(self) -> None:
        """Рисует сетку"""
        for digit in range(my_space.GRID_LIMIT):
            pygame.draw.line(my_space.screen, my_space.BLACK, (
                my_space.LEFT_MARGIN + self.offset * my_space.BLOCK_SIZE,
                my_space.UP_MARGIN + digit * my_space.BLOCK_SIZE),
                             (
                                 my_space.LEFT_MARGIN + (
                                         my_space.GRID_SIZE + self.offset) * my_space.BLOCK_SIZE,
                                 my_space.UP_MARGIN + digit * my_space.BLOCK_SIZE), 1)

            pygame.draw.line(my_space.screen, my_space.BLACK,
                             (my_space.LEFT_MARGIN +
                              (digit + self.offset) * my_space.BLOCK_SIZE, my_space.UP_MARGIN),
                             (my_space.LEFT_MARGIN + (digit + self.offset) * my_space.BLOCK_SIZE,
                              my_space.UP_MARGIN + my_space.GRID_SIZE * my_space.BLOCK_SIZE), 1)

    def __add_nums_letters(self) -> None:
        """
        Рисует цифры 1-10 по вертикали и добавляет буквы под горизонталью
        линии для обеих сеток
        """
        for digit in range(my_space.MAX_DIGIT):
            num_vertical = my_space.font.render(str(digit + 1), True, my_space.BLACK)
            letters_horizontal = my_space.font.render(
                my_space.LETTERS[digit], True, my_space.BLACK)
            num_vertical_width = num_vertical.get_width()
            num_vertical_height = num_vertical.get_height()
            letters_horizontal_width = letters_horizontal.get_width()

            my_space.screen.blit(num_vertical, (
                my_space.LEFT_MARGIN - (
                        my_space.BLOCK_SIZE // 2 + num_vertical_width // 2) +
                self.offset * my_space.BLOCK_SIZE,
                my_space.UP_MARGIN + digit * my_space.BLOCK_SIZE + (
                        my_space.BLOCK_SIZE // 2 - num_vertical_height // 2)))

            my_space.screen.blit(letters_horizontal,
                                 (my_space.LEFT_MARGIN + digit * my_space.BLOCK_SIZE + (
                                         my_space.BLOCK_SIZE // 2 - letters_horizontal_width // 2) +
                                  self.offset * my_space.BLOCK_SIZE,
                                  my_space.UP_MARGIN + my_space.GRID_SIZE * my_space.BLOCK_SIZE))

    def __sign(self) -> None:
        """
        Помещает имена игроков в центр над сетками
        """
        player = my_space.font.render(self.title, True, my_space.RED)
        sign_width = player.get_width()
        my_space.screen.blit(player,
                             (my_space.LEFT_MARGIN + 5 * my_space.BLOCK_SIZE - sign_width // 2 +
                              self.offset * my_space.BLOCK_SIZE,
                              my_space.UP_MARGIN - my_space.BLOCK_SIZE // 2 - my_space.FONT_SIZE))
