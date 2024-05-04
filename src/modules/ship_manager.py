import copy
import random
from typing import Set, List
from src.modules.point_class import Point
import src.global_variables as my_space


class ShipManager:
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
        """
        ships_grid = []
        for ship_size in range(1, my_space.SHIPS_LIMIT):
            for _ in range(my_space.SHIPS_LIMIT - ship_size):
                ship = self.create_ship(ship_size, self.available_blocks)
                ships_grid.append(ship)
                self.add_new_ship(set(ship))
                self.update_available_blocks(set(ship))
        return ships_grid


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
