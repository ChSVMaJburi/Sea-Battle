from typing import Tuple
import const_variable as const
import pygame

pygame.init()


class Button:
    """
    Создает кнопки и печатает пояснительное сообщение для них
    draw_button(): Рисует кнопку в виде цветного прямоугольника
    change_color_on_hover(): Рисует кнопку в виде прямоугольника зеленого цвета.
    """

    def __init__(self, x_ofs: int, button1: str):
        self.__tl = button1
        self.__tl_w, self.__tl_h = const.font.size(self.__tl)
        self.__button_w = self.__tl_w + const.BLOCK_SIZE
        self.__button_h = self.__tl_h + const.BLOCK_SIZE
        self.__x = x_ofs + const.BLOCK_SIZE
        self.__y = const.UP_MARGIN + const.BUTTON_BLOCK_OFFSET * \
                   const.BLOCK_SIZE + self.__button_h
        self.draw = self.__x, self.__y - const.TEXT_MARGIN, self.__button_w - const.BUTTON_MARGIN, self.__button_h
        self.rect = pygame.Rect(self.draw)
        self.__button_tl = self.__x + self.__button_w // 2 - self.__tl_w // 2 - \
                           const.TEXT_MARGIN, self.__y + self.__button_h // 2 - self.__tl_h // 2 - const.TEXT_MARGIN
        self.__cl = const.LIGHT_GRAY

    def draw_button(self, cl: Tuple[int, int, int] = None) -> None:
        """
        Рисует кнопку в виде цветного прямоугольника
        Аргументы:
            цвет (tuple): цвет кнопки. По умолчанию значение равно None
        """
        if not cl:
            cl = self.__cl
        pygame.draw.rect(const.screen, cl, self.draw)
        text = const.font.render(
            self.__tl, True, const.RED)
        const.screen.blit(text, self.__button_tl)

    def change_color_on_hover(self) -> None:
        """
        Изменение цвета кнопки при наведении курсора мыши на нее
        """
        coord = pygame.mouse.get_pos()
        if self.rect.collidepoint(coord):
            self.draw_button(const.GREY)
