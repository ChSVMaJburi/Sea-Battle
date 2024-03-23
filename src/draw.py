from typing import Set, List, Tuple
import global_variable as variables
from dotted_and_hit import dotted_and_hit
import pygame
import random

pygame.init()


class draw:
    def grid(offset: int) -> None:
        for i in range(11):
            pygame.draw.line(variables.screen, variables.BL, (
                variables.l_margin + offset * variables.block_sz, variables.upp_margin + i * variables.block_sz),
                             (variables.l_margin + (10 + offset) * variables.block_sz,
                              variables.upp_margin + i * variables.block_sz), 1)

            pygame.draw.line(variables.screen, variables.BL,
                             (variables.l_margin + (i + offset) * variables.block_sz, variables.upp_margin),
                             (variables.l_margin + (i + offset) * variables.block_sz,
                              variables.upp_margin + 10 * variables.block_sz), 1)

    def ship(ships_coor_list: List[Tuple[int, int]]) -> None:
        """
         Рисует прямоугольники вокруг блоков, занятых кораблем
         Аргументы:
         ships_coor_list (list of tuple): список координат судна
        """
        for i in ships_coor_list:
            ship = sorted(i)
            x_s = ship[0][0]
            y_s = ship[0][1]
            ship_w = variables.block_sz * len(ship)
            ship_h = variables.block_sz
            if len(ship) > 1 and ship[0][0] == ship[1][0]:
                ship_w, ship_h = ship_h, ship_w
            x = variables.block_sz * (x_s - 1) + variables.l_margin
            y = variables.block_sz * (y_s - 1) + variables.upp_margin
            if ships_coor_list == variables.human.ships:
                x += 15 * variables.block_sz
            pygame.draw.rect(variables.screen, variables.BL, ((
                                                                  x, y), (ship_w, ship_h)),
                             width=variables.block_sz // 10)

    def dotted(dotted: Set[Tuple[int, int]]) -> None:
        """
        Рисует точки в центре всех блоков в dotted
        """
        for i in dotted:
            pygame.draw.circle(variables.screen, variables.BL, (variables.block_sz * (
                    i[0] - 0.5) + variables.l_margin, variables.block_sz * (i[1] - 0.5) + variables.upp_margin),
                               variables.block_sz // 5)

    def destroyed_ships(pos: int, oppo_ships_list: List[Set[Tuple[int, int]]], comp_turn: bool,
                        diagonal_only: bool = False) -> None:
        """
        Добавляет блоки до и после корабля в dotted_set, чтобы нарисовать на них точки.
        Добавляет все блоки на корабле в hit_bl, установленные для рисования крестиков внутри разрушенного корабля.
        """
        if oppo_ships_list == variables.ship_w:
            ships_list = variables.computer.ships
        elif oppo_ships_list == variables.H_ships_w:
            ships_list = variables.human.ships
        ship = sorted(ships_list[pos])
        for i in range(-1, 1):
            dotted_and_hit(ship[i], comp_turn, diagonal_only)

    def hit_Bl(hit_Bl: Set[Tuple[int, int]]) -> None:
        """
        Рисует "X" в блоках, которые были успешно поражены либо компьютером, либо человеком
        """
        for block in hit_Bl:
            x1 = variables.block_sz * (block[0] - 1) + variables.l_margin
            y1 = variables.block_sz * (block[1] - 1) + variables.upp_margin
            pygame.draw.line(variables.screen, variables.BL, (x1, y1), (x1 +
                                                                        variables.block_sz, y1 + variables.block_sz),
                             variables.block_sz // 7)
            pygame.draw.line(variables.screen, variables.BL, (x1, y1 + variables.block_sz),
                             (x1 + variables.block_sz, y1), variables.block_sz // 7)


class ships(draw):
    def __init__(self):
        self.ava_Bl = set((a, b) for a in range(1, 11) for b in range(1, 11))
        self.ships_set = set()
        self.ships = self.grid()

    def create_ship(self, num_Bl: int, ava_Bl: Set[Tuple[int, int]]) -> List[Tuple[int, int]]:
        """
        Создает корабль заданной длины, начиная с начального блока
                , возвращенного предыдущим методом, используя тип корабля и направление, возвращенный предыдущим методом.
                Проверяет, является ли судно действительным и добавляет его в список кораблей.
        Аргументы:
            number_of_blocks (int): длина необходимого судна
            available_blocks (set): свободные блоки для создания кораблей
        Возвращается:
            список: список кортежей с координатами нового корабля
        """
        ship_coor = []
        x_y = random.randint(0, 1)
        str_rev = random.choice((-1, 1))
        x, y = random.choice(tuple(ava_Bl))
        for _ in range(num_Bl):
            ship_coor.append((x, y))
            if not x_y:
                str_rev, x = self.add_ship(
                    x, str_rev, x_y, ship_coor)
            else:
                str_rev, y = self.add_ship(
                    y, str_rev, x_y, ship_coor)
        ship = set(ship_coor)
        if ship.issubset(self.ava_Bl):
            return ship_coor
        return self.create_ship(num_Bl, ava_Bl)

    def add_ship(self, coor: int, str_rev: int, x_y: int, ship_coor: List[Tuple[int, int]]) -> Tuple[int, int]:
        if (coor <= 1 and str_rev == -1) or (coor >= 10 and str_rev == 1):
            str_rev *= -1
            return str_rev, ship_coor[0][x_y] + str_rev
        else:
            return str_rev, ship_coor[-1][x_y] + str_rev

    def add_new_ship(self, ship: Set[Tuple[int, int]]) -> None:
        """
        Добавляет все блоки в списке кораблей
        Аргументы:
            ship (set): список кортежей с координатами вновь созданного корабля
        """
        self.ships_set.update(ship)

    def update_ava_Bl(self, ship: Set[Tuple[int, int]]) -> None:
        """
        Удаляет все блоки, занятые кораблем и вокруг него, из набора доступных блоков
        Аргументы:
            ship (): список кортежей с координатами вновь созданного корабля
        """
        for i in ship:
            for j in range(-1, 2):
                for m in range(-1, 2):
                    if 0 < (i[0] + j) < 11 and 0 < (i[1] + m) < 11:
                        self.ava_Bl.discard((i[0] + j, i[1] + m))

    def grid(self) -> List[List[Tuple[int, int]]]:
        """
        Создает необходимое количество кораблей каждого типа.
                Добавляет каждый корабль в список кораблей.
        Возвращается:
            список: 2d-список всех кораблей
        """
        ships_coor = []
        for i in range(1, 5):
            for _ in range(5 - i):
                ship = self.create_ship(i, self.ava_Bl)
                ships_coor.append(ship)
                self.add_new_ship(ship)
                self.update_ava_Bl(ship)
        return ships_coor
