"""Реализация классов Drawer, ShipDrawer"""
import copy
from typing import Set, List, Tuple, Iterator
import random
import pygame
import global_variables as my_space


class Point:
    """Класс схожий с Tuple[int, int] для упрощения кода"""

    def __init__(self, x_coordinate: int, y_coordinate: int) -> None:
        self.coordinate = (x_coordinate, y_coordinate)

    def __lt__(self, other: 'Point') -> bool:
        return self.coordinate < other.coordinate

    def __getitem__(self, index: int) -> int:
        return self.coordinate[index]

    def __iter__(self) -> Iterator[Tuple[int, int]]:
        return iter(self.coordinate)

    def __repr__(self) -> str:
        return f"{self.coordinate[0]} {self.coordinate[1]}"

    def __eq__(self, other: 'Point') -> bool:
        return self.coordinate == other.coordinate

    def __ne__(self, other: 'Point') -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return hash((self.coordinate, self.coordinate))

    def __is__(self, other: 'Point') -> bool:
        return self == other


class Drawer:
    """Рисовальщик, рисует на поле нужные знаки, фигуры"""

    @staticmethod
    def draw_ship(ships_coord_list: List[Tuple[Point, Point]],
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


def next_coordinate(coordinate: int, add: int, coord_x_or_y: int,
                    ship_coordinate: List[Point]) -> Point:
    """Вычисляет следующую координату корабля в заданном направлении на основе
    текущей координаты и направления движения"""
    if (coordinate <= 1 and add == -1) or (coordinate >= my_space.GRID_SIZE and add == 1):
        add *= -1
        return Point(add, ship_coordinate[0][coord_x_or_y] + add)
    return Point(add, ship_coordinate[-1][coord_x_or_y] + add)


def is_valid_coordinate(x_coordinate: int, y_coordinate: int) -> bool:
    """
    Проверяет, являются ли координаты корректными для игрового поля.
    """
    return 1 <= x_coordinate <= my_space.GRID_SIZE and 1 <= y_coordinate <= my_space.GRID_SIZE


class ShipDrawer(Drawer):
    """Создаёт корабли и делает операции связанные с их состоянием"""

    def __init__(self):
        self.available_blocks = set(
            Point(x_coord, y_coord) for x_coord in range(1, my_space.GRID_LIMIT) for y_coord in
            range(1, my_space.GRID_LIMIT))
        self.ships_set = set()
        self.ships = self.generate_ships_grid()
        self.ships_copy = copy.deepcopy(self.ships)

    def create_ship(self, num_blocks: int, available_blocks: Set[Point]) -> List[Point]:
        """
        Генерирует координаты для корабля заданной длины, учитывая доступные блоки на игровом поле.
        """
        # print(num_blocks, len(available_blocks))
        ship_coord = list[Point]()
        coord_x_or_y = random.randint(0, 1)
        add = random.choice((-1, 1))
        # print(tuple(available_blocks))
        # print(available_blocks)
        x_coordinate, y_coordinate = random.choice(tuple(available_blocks))
        for _ in range(num_blocks):
            ship_coord.append(Point(x_coordinate, y_coordinate))
            if not coord_x_or_y:
                add, x_coordinate = next_coordinate(
                    x_coordinate, add, coord_x_or_y, ship_coord)
            else:
                add, y_coordinate = next_coordinate(
                    y_coordinate, add, coord_x_or_y, ship_coord)
        ship = set(ship_coord)
        if ship.issubset(self.available_blocks):
            return ship_coord
        return self.create_ship(num_blocks, available_blocks)

    def add_new_ship(self, ship: Set[Point]) -> None:
        """
        Добавляет все блоки в списке кораблей
        Аргументы:
            ship (set): список кортежей с координатами вновь созданного корабля
        """
        self.ships_set.update(ship)

    def update_available_blocks(self, ship_coordinates: Set[Point]) -> None:
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
                        self.available_blocks.discard(Point(neighbor_x, neighbor_y))

    def generate_ships_grid(self) -> List[List[Point]]:
        """
        Генерирует необходимое количество кораблей каждого типа.
        Добавляет каждый корабль в список кораблей.
        Возвращает 2D-список всех кораблей.
        """
        ships_grid = []
        for ship_size in range(1, my_space.SHIPS_LIMIT):
            for _ in range(my_space.SHIPS_LIMIT - ship_size):
                ship = self.create_ship(ship_size, self.available_blocks)
                ships_grid.append(ship)
                self.add_new_ship(set(ship))
                self.update_available_blocks(set(ship))
        return ships_grid
