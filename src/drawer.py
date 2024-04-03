"""Реализация классов Drawer, ShipDrawer"""
from typing import Set, List, Tuple
import random
import pygame
import const_variables as const
from dotted_and_hit import dotted_and_hit


def draw_grid(offset: int) -> None:
    """Рисует сетку"""
    for digit in range(const.GRID_LIMIT):
        pygame.draw.line(const.screen, const.BLACK, (
            const.LEFT_MARGIN + offset * const.BLOCK_SIZE,
            const.UP_MARGIN + digit * const.BLOCK_SIZE),
                         (const.LEFT_MARGIN + (const.GRID_SIZE + offset) * const.BLOCK_SIZE,
                          const.UP_MARGIN + digit * const.BLOCK_SIZE), 1)

        pygame.draw.line(const.screen, const.BLACK,
                         (const.LEFT_MARGIN +
                          (digit + offset) * const.BLOCK_SIZE, const.UP_MARGIN),
                         (const.LEFT_MARGIN + (digit + offset) * const.BLOCK_SIZE,
                          const.UP_MARGIN + const.GRID_SIZE * const.BLOCK_SIZE), 1)


class Drawer:
    """Рисовальщик, рисует на поле нужные знаки, фигуры"""

    def draw_ship(ships_coord_list: List[Tuple[Tuple[int, int], Tuple[int, int]]]) -> None:
        """
         Рисует прямоугольники вокруг блоков, занятых кораблем
         Аргументы:
         ships_coord_list (list of tuple): список координат судна
        """
        for cur_coord in ships_coord_list:
            coordinates = sorted(cur_coord)
            x_index = coordinates[0][0]
            y_index = coordinates[0][1]
            ship_width = const.BLOCK_SIZE * len(coordinates)
            ship_height = const.BLOCK_SIZE
            if len(coordinates) > 1 and coordinates[0][0] == coordinates[1][0]:
                ship_width, ship_height = ship_height, ship_width
            x_coord = const.BLOCK_SIZE * (x_index - 1) + const.LEFT_MARGIN
            y_coord = const.BLOCK_SIZE * (y_index - 1) + const.UP_MARGIN
            if ships_coord_list == const.HUMAN.ships:
                x_coord += const.DISTANCE * const.BLOCK_SIZE
            pygame.draw.rect(const.screen, const.BLACK,
                             ((x_coord, y_coord), (ship_width, ship_height)),
                             width=const.BLOCK_SIZE // const.GRID_SIZE)

    def draw_dots(dots: Set[Tuple[int, int]]) -> None:
        """
        Рисует точки в центре всех блоков в dots
        """
        for dot in dots:
            pygame.draw.circle(const.screen, const.BLACK, (
                const.BLOCK_SIZE * (dot[0] - 0.5) + const.LEFT_MARGIN,
                const.BLOCK_SIZE * (dot[1] - 0.5) + const.UP_MARGIN),
                               const.BLOCK_SIZE // const.SHIPS_LIMIT)

    def process_destroyed_ship(pos: int, opponent_ships: List[Set[Tuple[int, int]]],
                               computer_turn: bool, diagonal_only: bool = False) -> None:
        """
        Добавляет блоки до и после корабля в dotted_set, чтобы нарисовать на них точки.
        Добавляет все блоки на корабле в hit_blocks, установленные для рисования крестиков внутри
        разрушенного корабля.
        """
        ships_list = const.HUMAN.ships
        if opponent_ships == const.COMPUTER_SHIPS:
            ships_list = const.COMPUTER.ships
        ship = sorted(ships_list[pos])
        for ind in range(-1, 1):
            dotted_and_hit(ship[ind], computer_turn, diagonal_only)

    def hit_blocks(hit_blocks: Set[Tuple[int, int]]) -> None:
        """
        Рисует "X" в блоках, которые были успешно поражены либо компьютером, либо человеком
        """
        for block in hit_blocks:
            x_coordinate = const.BLOCK_SIZE * (block[0] - 1) + const.LEFT_MARGIN
            y_coordinate = const.BLOCK_SIZE * (block[1] - 1) + const.UP_MARGIN
            pygame.draw.line(const.screen, const.BLACK, (x_coordinate, y_coordinate),
                             (x_coordinate + const.BLOCK_SIZE, y_coordinate + const.BLOCK_SIZE),
                             const.BLOCK_SIZE // const.SEVEN)
            pygame.draw.line(const.screen, const.BLACK,
                             (x_coordinate, y_coordinate + const.BLOCK_SIZE),
                             (x_coordinate + const.BLOCK_SIZE, y_coordinate),
                             const.BLOCK_SIZE // const.SEVEN)


def add_ship(coordinate: int, add: int, coord_x_or_y: int,
             ship_coordinate: List[Tuple[int, int]]) -> Tuple[int, int]:
    """Вычисляет следующую координату корабля в заданном направлении на основе
    текущей координаты и направления движения"""
    if (coordinate <= 1 and add == -1) or (coordinate >= const.MAX_DIGIT and add == 1):
        add *= -1
        return add, ship_coordinate[0][coord_x_or_y] + add
    return add, ship_coordinate[-1][coord_x_or_y] + add


def is_valid_coordinate(x_coordinate: int, y_coordinate: int) -> bool:
    """
    Проверяет, являются ли координаты корректными для игрового поля.
    """
    return 1 <= x_coordinate <= const.MAX_DIGIT and 1 <= y_coordinate <= const.MAX_DIGIT


class ShipDrawer(Drawer):
    """Создаёт корабли и делает операции связанные с их состоянием"""

    def __init__(self):
        """Инициализация"""
        self.available_blocks = set(
            (x_coord, y_coord) for x_coord in range(1, const.GRID_LIMIT) for y_coord in
            range(1, const.GRID_LIMIT))
        self.ships_set = set()
        self.ships = self.generate_ships_grid()

    def create_ship(self, num_blocks: int, available_blocks: Set[Tuple[int, int]]) \
            -> List[Tuple[int, int]]:
        """
        Создает корабль заданной длины, начиная с начального блока, возвращенного предыдущим
        методом, используя тип корабля и направление, возвращенный предыдущим методом.
        Проверяет, является ли судно действительным и добавляет его в список кораблей.
        """
        ship_coord = []
        coord_x_or_y = random.randint(0, 1)
        add = random.choice((-1, 1))
        x_coordinate, y_coordinate = random.choice(tuple(available_blocks))
        for _ in range(num_blocks):
            ship_coord.append((x_coordinate, y_coordinate))
            if not coord_x_or_y:
                add, x_coordinate = add_ship(
                    x_coordinate, add, coord_x_or_y, ship_coord)
            else:
                add, y_coordinate = add_ship(
                    y_coordinate, add, coord_x_or_y, ship_coord)
        ship = set(ship_coord)
        if ship.issubset(self.available_blocks):
            return ship_coord
        return self.create_ship(num_blocks, available_blocks)

    def add_new_ship(self, ship: Set[Tuple[int, int]]) -> None:
        """
        Добавляет все блоки в списке кораблей
        Аргументы:
            ship (set): список кортежей с координатами вновь созданного корабля
        """
        self.ships_set.update(ship)

    def update_available_blocks(self, ship_coordinates: Set[Tuple[int, int]]) -> None:
        """
        Удаляет все блоки, занятые кораблем и расположенные вокруг него, из набора доступных блоков.
        Аргументы:
            ship_coordinates: набор координат корабля (кортежи с координатами X и Y)
        """
        for coord in ship_coordinates:
            for offset_x in range(-1, 2):
                for offset_y in range(-1, 2):
                    neighbor_x = coord[0] + offset_x
                    neighbor_y = coord[1] + offset_y

                    if is_valid_coordinate(neighbor_x, neighbor_y):
                        self.available_blocks.discard((neighbor_x, neighbor_y))

    def generate_ships_grid(self) -> List[List[Tuple[int, int]]]:
        """
        Генерирует необходимое количество кораблей каждого типа.
        Добавляет каждый корабль в список кораблей.
        Возвращает 2D-список всех кораблей.
        """
        ships_grid = []
        for ship_size in range(1, const.SHIPS_LIMIT):
            for _ in range(const.SHIPS_LIMIT - ship_size):
                ship = self.create_ship(ship_size, self.available_blocks)
                ships_grid.append(ship)
                self.add_new_ship(ship)
                self.update_available_blocks(ship)
        return ships_grid
