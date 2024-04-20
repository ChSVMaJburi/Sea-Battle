"""Реализация класса Drawer"""
from typing import Set, List, Tuple
import pygame
import src.global_variables as my_space
from src.modules.ship_manager import Point


class Drawer:
    """Рисовальщик, рисует на поле нужные знаки, фигуры"""

    @staticmethod
    def draw_rectangles(ships_coord_list: List[Tuple[Point, Point]],
                        offset: int) -> None:
        """
         Рисует прямоугольники вокруг блоков, занятых кораблем
         Аргументы:
         ships_coord_list (list of tuple): список координат судна
        """
        for cur_coord in ships_coord_list:
            coordinates = sorted(cur_coord)
            x_index = coordinates[0][0]
            y_index = coordinates[0][1]
            ship_width = my_space.BLOCK_SIZE * len(coordinates)
            ship_height = my_space.BLOCK_SIZE
            if len(coordinates) > 1 and coordinates[0][0] == coordinates[1][0]:
                ship_width, ship_height = ship_height, ship_width
            x_coord = my_space.BLOCK_SIZE * (x_index - 1) + my_space.LEFT_MARGIN
            y_coord = my_space.BLOCK_SIZE * (y_index - 1) + my_space.UP_MARGIN
            x_coord += offset * my_space.BLOCK_SIZE
            pygame.draw.rect(my_space.screen, my_space.BLACK,
                             ((x_coord, y_coord), (ship_width, ship_height)),
                             width=my_space.BLOCK_SIZE // my_space.GRID_SIZE)

    @staticmethod
    def draw_dots(dots: Set[Point]) -> None:
        """
        Рисует точки в центре всех блоков в dots
        """
        for dot in dots:
            pygame.draw.circle(my_space.screen, my_space.BLACK, (
                my_space.BLOCK_SIZE * (dot[0] - 0.5) + my_space.LEFT_MARGIN,
                my_space.BLOCK_SIZE * (dot[1] - 0.5) + my_space.UP_MARGIN),
                               my_space.BLOCK_SIZE // my_space.SHIPS_LIMIT)

    @staticmethod
    def draw_hit_blocks(hit_blocks: Set[Point]) -> None:
        """
        Рисует "X" в блоках, которые были успешно поражены либо компьютером, либо человеком
        """
        for block in hit_blocks:
            x_coordinate = my_space.BLOCK_SIZE * (block[0] - 1) + my_space.LEFT_MARGIN
            y_coordinate = my_space.BLOCK_SIZE * (block[1] - 1) + my_space.UP_MARGIN
            pygame.draw.line(my_space.screen, my_space.BLACK, (x_coordinate, y_coordinate),
                             (x_coordinate + my_space.BLOCK_SIZE, y_coordinate +
                              my_space.BLOCK_SIZE), my_space.BLOCK_SIZE // my_space.DIVIDE)
            pygame.draw.line(my_space.screen, my_space.BLACK,
                             (x_coordinate, y_coordinate + my_space.BLOCK_SIZE),
                             (x_coordinate + my_space.BLOCK_SIZE, y_coordinate),
                             my_space.BLOCK_SIZE // my_space.DIVIDE)
