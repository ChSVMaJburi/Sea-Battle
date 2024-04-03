"""Реализуется класс Button"""
from typing import Tuple
import pygame
import const_variables as const


class Button:
    """
    Создает кнопки и печатает пояснительное сообщение для них
    draw_button(): Рисует кнопку в виде цветного прямоугольника
    change_color_on_hover(): Рисует кнопку в виде прямоугольника зеленого цвета.
    """

    def __init__(self, x_offset: int, text: str):
        self.text = text
        self.text_width, self.text_height = const.font.size(self.text)
        self.button_width = self.text_width + const.BLOCK_SIZE
        self.button_height = self.text_height + const.BLOCK_SIZE
        self.x_coordinate = x_offset + const.BLOCK_SIZE
        self.y_coordinate = (const.UP_MARGIN + const.BUTTON_BLOCK_OFFSET * const.BLOCK_SIZE +
                             self.button_height)
        self.draw = (self.x_coordinate, self.y_coordinate - const.TEXT_MARGIN,
                     self.button_width - const.BUTTON_MARGIN, self.button_height)
        self.rect = pygame.Rect(self.draw)
        self.text_position = (
            self.x_coordinate + self.button_width // 2 - self.text_width // 2 - const.TEXT_MARGIN,
            self.y_coordinate + self.button_height // 2 - self.text_height // 2 - const.TEXT_MARGIN)
        self.default_color = const.LIGHT_GRAY

    def draw_button(self, color: Tuple[int, int, int] = None) -> None:
        """
        Рисует кнопку в виде цветного прямоугольника
        Аргументы:
            цвет (tuple): цвет кнопки. По умолчанию значение равно None
        """
        if not color:
            color = self.default_color
        pygame.draw.rect(const.screen, color, self.draw)
        text = const.font.render(self.text, True, const.RED)
        const.screen.blit(text, self.text_position)

    def change_color_on_hover(self) -> None:
        """
        Изменение цвета кнопки при наведении курсора мыши на нее
        """
        coord = pygame.mouse.get_pos()
        if self.rect.collidepoint(coord):
            self.draw_button(const.GREY)
