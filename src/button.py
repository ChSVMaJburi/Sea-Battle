from typing import Tuple
import global_variable as glob
import pygame

pygame.init()


class button:
    """
    Создает кнопки и печатает пояснительное сообщение для них
    draw_button(): Рисует кнопку в виде цветного прямоугольника
    change_color_on_hover(): Рисует кнопку в виде прямоугольника зеленого цвета.
    """

    def __init__(self, x_ofs: int, button1: str):
        self.__tl = button1
        self.__tl_w, self.__tl_h = glob.font.size(self.__tl)
        self.__button_w = self.__tl_w + glob.block_sz
        self.__button_h = self.__tl_h + glob.block_sz
        self.__x = x_ofs + glob.block_sz
        self.__y = glob.upp_margin + glob.BUTTON_BLOCK_OFFSET * \
                   glob.block_sz + self.__button_h
        self.draw = self.__x, self.__y - glob.TEXT_MARGIN, self.__button_w - glob.BUTTON_MARGIN, self.__button_h
        self.rect = pygame.Rect(self.draw)
        self.__button_tl = self.__x + self.__button_w // 2 - self.__tl_w // 2 - \
                           glob.TEXT_MARGIN, self.__y + self.__button_h // 2 - self.__tl_h // 2 - glob.TEXT_MARGIN
        self.__cl = glob.L_GRAY

    def draw_button(self, cl: Tuple[int, int, int] = None) -> None:
        """
        Рисует кнопку в виде цветного прямоугольника
        Аргументы:
            цвет (tuple): цвет кнопки. По умолчанию значение равно None
        """
        if not cl:
            cl = self.__cl
        pygame.draw.rect(glob.screen, cl, self.draw)
        text = glob.font.render(
            self.__tl, True, glob.RED)
        glob.screen.blit(text, self.__button_tl)

    def change_color_on_hover(self) -> None:
        """
        Изменение цвета кнопки при наведении курсора мыши на нее
        """
        coord = pygame.mouse.get_pos()
        if self.rect.collidepoint(coord):
            self.draw_button(glob.GR)
