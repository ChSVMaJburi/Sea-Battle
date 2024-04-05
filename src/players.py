"""Реализуем классы Player, HumanPlayer"""
from abc import ABC, abstractmethod
from typing import List
import pygame
import global_variables as my_space
from grid_class import Grid
from drawer import ShipDrawer, Point


class Player(ABC):
    """Реализуем класс Player"""

    def __init__(self, name: str, offset: int):
        self.name = name
        self.offset = offset
        self.create_board()
        self.drawer = ShipDrawer()
        self.hit_blocks = set[Point]()
        self.dotted = set[Point]()

    def create_board(self):
        """Начинает процесс рисования доски"""
        Grid(self.name, self.offset)

    @abstractmethod
    def update_dotted_and_hit(self, shot_coordinates: Point,
                              diagonal_only: bool) -> None:
        """Эта процедура добавляет точки вокруг клетки, в которую был произведен выстрел"""

    @abstractmethod
    def shoot(self, other_player, game_over: bool, shot_taken: bool) -> tuple[bool, bool, bool]:
        """Обрабатывает события мыши для игрового поля и определяет, чей сейчас ход.
               В зависимости от событий, она обновляет состояние игры"""

    def process_destroyed_ship(self, pos: int, other_player, diagonal_only: bool) -> None:
        """
        Обрабатывает процесс уничтожения корабля
        """
        ship = sorted(other_player.drawer.ships[pos])
        for ind in range(-1, 1):
            self.update_dotted_and_hit(ship[ind], diagonal_only)


def handle_mouse_event(event: pygame.event) -> Point or None:
    """Обрабатывает события мыши для хода игрока."""
    if event.type == pygame.MOUSEBUTTONDOWN:
        x_coordinate, y_coordinate = event.pos
        if (my_space.MIN_X <= x_coordinate <= my_space.MAX_X and
                my_space.MIN_Y <= y_coordinate <= my_space.MAX_Y):
            if ((my_space.LEFT_MARGIN < x_coordinate < my_space.LEFT_MARGIN +
                 my_space.GRID_SIZE * my_space.BLOCK_SIZE) and
                    (my_space.UP_MARGIN < y_coordinate < my_space.UP_MARGIN +
                     my_space.GRID_SIZE * my_space.BLOCK_SIZE)):
                return Point((x_coordinate - my_space.LEFT_MARGIN) // my_space.BLOCK_SIZE + 1,
                             (y_coordinate - my_space.UP_MARGIN) // my_space.BLOCK_SIZE + 1)
    return None


class HumanPlayer(Player):
    """Реализуем класс HumanPlayer"""

    def __init__(self, name: str, offset: int):
        super().__init__(name, offset)
        self.destroyed_ships = list[List[Point]]()

    def update_dotted_and_hit(self, shot_coordinates: Point,
                              diagonal_only: bool) -> None:
        """Эта процедура добавляет точки вокруг клетки, в которую был произведен выстрел"""
        fire_x_coordinate, fire_y_coordinate = shot_coordinates
        min_x, max_x = 0, my_space.GRID_LIMIT
        self.hit_blocks.add(Point(fire_x_coordinate, fire_y_coordinate))
        for add_x_coordinate in range(-1, 2):
            for add_y_coordinate in range(-1, 2):
                if (not diagonal_only and min_x < fire_x_coordinate + add_x_coordinate < max_x and
                        0 < fire_y_coordinate + add_y_coordinate < my_space.GRID_LIMIT):
                    self.dotted.add(Point(fire_x_coordinate + add_x_coordinate,
                                          fire_y_coordinate + add_y_coordinate))
        self.dotted -= self.hit_blocks

    def shoot(self, other_player: Player, game_over: bool, shot_taken: bool) \
            -> tuple[bool, bool, bool]:
        """Обрабатывает события мыши для игрового поля и определяет, чей сейчас ход.
               В зависимости от событий, она обновляет состояние игры"""
        other_turn = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True, True, shot_taken
            shot_coordinates = handle_mouse_event(event)
            if shot_coordinates is not None:
                shot_taken = False
                for hit_block in self.hit_blocks:
                    if hit_block == shot_coordinates:
                        shot_taken = True
                for dot in self.dotted:
                    if dot == shot_coordinates:
                        shot_taken = True
                if not shot_taken:
                    other_turn = not self.__check_is_successful_hit(shot_coordinates, other_player)
        return game_over, other_turn, shot_taken

    def __check_is_successful_hit(self, shot_coordinates: Point, other_player: Player) -> bool:
        """Проверяет попадание в корабль противника и выполняет соответствующие действия.
        Возвращает True при попадании, иначе False."""
        for ship in other_player.drawer.ships_copy:
            if shot_coordinates in ship:
                self.update_dotted_and_hit(shot_coordinates, True)
                position = other_player.drawer.ships_copy.index(ship)
                if len(ship) == 1:
                    self.update_dotted_and_hit(shot_coordinates, True)
                ship.remove(shot_coordinates)
                other_player.drawer.ships_set.discard(shot_coordinates)
                if not ship:
                    self.process_destroyed_ship(position, other_player, False)
                    # print(type(other_player.drawer.ships[position][0]))
                    self.destroyed_ships.append(other_player.drawer.ships[position])
                return True

        self.dotted.add(shot_coordinates)
        return False
