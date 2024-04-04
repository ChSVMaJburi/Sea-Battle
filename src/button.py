"""Реализуется класс Button"""
from typing import Tuple
import pygame
import global_variables as my_space


def init_pygame() -> None:
    """Проделаем стартовые операции pygame"""
    my_space.screen = pygame.display.set_mode(my_space.SIZE)
    my_space.FONT_SIZE = int(my_space.BLOCK_SIZE / 1.5)
    my_space.font = pygame.font.SysFont('notosans', my_space.FONT_SIZE)
    my_space.GAME_OVER = pygame.font.SysFont('notosans', 3 * my_space.BLOCK_SIZE)
    my_space.screen.fill(my_space.BLUE)
    pygame.display.set_caption("Sea Battle")


class Button:
    """
    Создает кнопки и печатает пояснительное сообщение для них
    draw_button(): Рисует кнопку в виде цветного прямоугольника
    change_color_on_hover(): Рисует кнопку в виде прямоугольника зеленого цвета.
    """

    def __init__(self, x_offset: int, text: str):
        if not my_space.is_pygame_init:
            init_pygame()
        self.text = text
        self.text_width, self.text_height = my_space.font.size(self.text)
        self.button_width = self.text_width + my_space.BLOCK_SIZE
        self.button_height = self.text_height + my_space.BLOCK_SIZE
        self.x_coordinate = x_offset + my_space.BLOCK_SIZE
        self.y_coordinate = (
                my_space.UP_MARGIN + my_space.BUTTON_BLOCK_OFFSET * my_space.BLOCK_SIZE +
                self.button_height)
        self.draw = (self.x_coordinate, self.y_coordinate - my_space.TEXT_MARGIN,
                     self.button_width - my_space.BUTTON_MARGIN, self.button_height)
        self.rect = pygame.Rect(self.draw)
        self.text_position = (
            self.x_coordinate + self.button_width // 2 - self.text_width // 2 - my_space.TEXT_MARGIN,
            self.y_coordinate + self.button_height // 2 - self.text_height // 2 - my_space.TEXT_MARGIN)
        self.default_color = my_space.LIGHT_GRAY

    def draw_button(self, color: Tuple[int, int, int] = None) -> None:
        """
        Рисует кнопку в виде цветного прямоугольника
        Аргументы:
            цвет (tuple): цвет кнопки. По умолчанию значение равно None
        """
        if not color:
            color = self.default_color
        pygame.draw.rect(my_space.screen, color, self.draw)
        text = my_space.font.render(self.text, True, my_space.RED)
        my_space.screen.blit(text, self.text_position)

    def change_color_on_hover(self) -> None:
        """
        Изменение цвета кнопки при наведении курсора мыши на нее
        """
        coord = pygame.mouse.get_pos()
        if self.rect.collidepoint(coord):
            self.draw_button(my_space.GREY)
