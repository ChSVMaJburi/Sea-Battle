from typing import Set, List, Tuple
import global_variable as my_space
from dotted_and_hit import dotted_and_hit
import pygame
import random

pygame.init()


class Drawer:
    def grid(offset: int) -> None:
        for i in range(11):
            pygame.draw.line(my_space.screen, my_space.BL, (
                my_space.l_margin + offset * my_space.block_sz, my_space.upp_margin + i * my_space.block_sz),
                             (my_space.l_margin + (my_space.GRID_SIZE + offset) * my_space.block_sz,
                              my_space.upp_margin + i * my_space.block_sz), 1)

            pygame.draw.line(my_space.screen, my_space.BL,
                             (my_space.l_margin + (i + offset) * my_space.block_sz, my_space.upp_margin),
                             (my_space.l_margin + (i + offset) * my_space.block_sz,
                              my_space.upp_margin + my_space.GRID_SIZE * my_space.block_sz), 1)

    def ship(ships_coord_list: List[Tuple[int, int]]) -> None:
        """
         Рисует прямоугольники вокруг блоков, занятых кораблем
         Аргументы:
         ships_coord_list (list of tuple): список координат судна
        """
        for cur_coord in ships_coord_list:
            ship = sorted(cur_coord)
            x_s = ship[0][0]
            y_s = ship[0][1]
            ship_w = my_space.block_sz * len(ship)
            ship_h = my_space.block_sz
            if len(ship) > 1 and ship[0][0] == ship[1][0]:
                ship_w, ship_h = ship_h, ship_w
            x = my_space.block_sz * (x_s - 1) + my_space.l_margin
            y = my_space.block_sz * (y_s - 1) + my_space.upp_margin
            if ships_coord_list == my_space.human.ships:
                x += 15 * my_space.block_sz
            pygame.draw.rect(my_space.screen, my_space.BL, ((
                                                        x, y), (ship_w, ship_h)),
                             width=my_space.block_sz // my_space.GRID_SIZE)

    def dotted(dotted: Set[Tuple[int, int]]) -> None:
        """
        Рисует точки в центре всех блоков в dotted
        """
        for i in dotted:
            pygame.draw.circle(my_space.screen, my_space.BL, (my_space.block_sz * (
                    i[0] - 0.5) + my_space.l_margin, my_space.block_sz * (i[1] - 0.5) + my_space.upp_margin),
                               my_space.block_sz // my_space.FIVE)

    def destroyed_ships(pos: int, opponent_ships: List[Set[Tuple[int, int]]], comp_turn: bool,
                        diagonal_only: bool = False) -> None:
        """
        Добавляет блоки до и после корабля в dotted_set, чтобы нарисовать на них точки.
        Добавляет все блоки на корабле в hit_blocks, установленные для рисования крестиков внутри разрушенного корабля.
        """
        if opponent_ships == my_space.ship_w:
            ships_list = my_space.computer.ships
        elif opponent_ships == my_space.H_ships_w:
            ships_list = my_space.human.ships
        ship = sorted(ships_list[pos])
        for i in range(-1, 1):
            dotted_and_hit(ship[i], comp_turn, diagonal_only)

    def hit_blocks(hit_blocks: Set[Tuple[int, int]]) -> None:
        """
        Рисует "X" в блоках, которые были успешно поражены либо компьютером, либо человеком
        """
        for block in hit_blocks:
            x1 = my_space.block_sz * (block[0] - 1) + my_space.l_margin
            y1 = my_space.block_sz * (block[1] - 1) + my_space.upp_margin
            pygame.draw.line(my_space.screen, my_space.BL, (x1, y1), (x1 +
                                                              my_space.block_sz, y1 + my_space.block_sz),
                             my_space.block_sz // my_space.SEVEN)
            pygame.draw.line(my_space.screen, my_space.BL, (x1, y1 + my_space.block_sz),
                             (x1 + my_space.block_sz, y1), my_space.block_sz // my_space.SEVEN)


class ShipDrawer(Drawer):
    def __init__(self):
        self.available_blocks = set((a, b) for a in range(1, 11) for b in range(1, 11))
        self.ships_set = set()
        self.ships = self.grid()

    def create_ship(self, num_blocks: int, available_blocks: Set[Tuple[int, int]]) -> List[Tuple[int, int]]:
        """
        Создает корабль заданной длины, начиная с начального блока
                , возвращенного предыдущим методом, используя тип корабля и направление, возвращенный предыдущим методом.
                Проверяет, является ли судно действительным и добавляет его в список кораблей.
        """
        ship_coord = []
        x_y = random.randint(0, 1)
        str_rev = random.choice((-1, 1))
        x, y = random.choice(tuple(available_blocks))
        for _ in range(num_blocks):
            ship_coord.append((x, y))
            if not x_y:
                str_rev, x = self.add_ship(
                    x, str_rev, x_y, ship_coord)
            else:
                str_rev, y = self.add_ship(
                    y, str_rev, x_y, ship_coord)
        ship = set(ship_coord)
        if ship.issubset(self.available_blocks):
            return ship_coord
        return self.create_ship(num_blocks, available_blocks)

    def add_ship(self, coor: int, str_rev: int, x_y: int, ship_coord: List[Tuple[int, int]]) -> Tuple[int, int]:
        if (coor <= 1 and str_rev == -1) or (coor >= 10 and str_rev == 1):
            str_rev *= -1
            return str_rev, ship_coord[0][x_y] + str_rev
        else:
            return str_rev, ship_coord[-1][x_y] + str_rev

    def add_new_ship(self, ship: Set[Tuple[int, int]]) -> None:
        """
        Добавляет все блоки в списке кораблей
        Аргументы:
            ship (set): список кортежей с координатами вновь созданного корабля
        """
        self.ships_set.update(ship)

    def update_available_blocks(self, ship: Set[Tuple[int, int]]) -> None:
        """
        Удаляет все блоки, занятые кораблем и вокруг него, из набора доступных блоков
        Аргументы:
            ship (): список кортежей с координатами вновь созданного корабля
        """
        for i in ship:
            for j in range(-1, 2):
                for m in range(-1, 2):
                    if 0 < (i[0] + j) < 11 and 0 < (i[1] + m) < 11:
                        self.available_blocks.discard((i[0] + j, i[1] + m))

    def grid(self) -> List[List[Tuple[int, int]]]:
        """
        Создает необходимое количество кораблей каждого типа.
                Добавляет каждый корабль в список кораблей.
        Возвращается: список: 2d-список всех кораблей
        """
        ships_coor = []
        for i in range(1, 5):
            for _ in range(5 - i):
                ship = self.create_ship(i, self.available_blocks)
                ships_coor.append(ship)
                self.add_new_ship(ship)
                self.update_available_blocks(ship)
        return ships_coor
