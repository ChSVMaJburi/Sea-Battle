"""Реализуем классы Player, HumanPlayer"""
import copy
from abc import ABC, abstractmethod
from typing import Tuple
from src.GUI.gui_drawer import Point
from src.modules.ship_manager import ShipManager
import src.global_variables as my_space


class Player(ABC):
    """Реализуем класс Player"""

    def __init__(self, offset: int):
        self.offset = offset
        self.ship_manager = ShipManager()
        self.hit_blocks = set[Point]()
        self.dotted = set[Point]()
        self.injured = set[Point]()
        self.missed = set[Point]()
        self.to_shot = set[Point]()
        self.dotted_to_shot = set[Point]()
        self.last_hits = list[Point]()
        self.destroyed_ships = list[list[Point]]()

    def update_dotted_and_hit(self, shot_coordinates: Point,
                              diagonal_only: bool) -> None:
        """Этот метод определяет точки, в которые уже нет смысла стрелять"""
        fire_x_coordinate, fire_y_coordinate = shot_coordinates
        min_x, max_x = self.offset, self.offset + my_space.GRID_LIMIT
        fire_x_coordinate += self.offset
        self.to_shot.add(shot_coordinates)
        self.hit_blocks.add(Point(fire_x_coordinate, fire_y_coordinate))
        for add_x_coordinate in range(-1, 2):
            for add_y_coordinate in range(-1, 2):
                if (not diagonal_only and min_x < fire_x_coordinate + add_x_coordinate < max_x and
                        0 < fire_y_coordinate + add_y_coordinate < my_space.GRID_LIMIT):
                    self.dotted.add(Point(fire_x_coordinate + add_x_coordinate,
                                          fire_y_coordinate + add_y_coordinate))
                    self.dotted_to_shot.add(Point(shot_coordinates[0] + add_x_coordinate,
                                                  fire_y_coordinate + add_y_coordinate))
        self.dotted -= self.hit_blocks

    def process_after_shoot(self, shoot: Point, is_hit: bool, is_destroyed: bool) -> None:
        """Проводит все нужные изменения после выстрела"""
        if not is_hit:
            self.dotted.add(Point(shoot[0] + self.offset, shoot[1]))
            self.dotted_to_shot.add(shoot)
        elif not is_destroyed:
            self.update_dotted_and_hit(shoot, True)
            self.last_hits.append(shoot)
        else:
            self.last_hits.append(shoot)
            for ind in range(-1, 1):
                self.update_dotted_and_hit(self.last_hits[ind], False)
            self.destroyed_ships.append(copy.deepcopy(self.last_hits))
            self.last_hits.clear()

    def check_is_successful_hit(self, shoot: Point) -> Tuple[bool, bool]:
        """Проверяет попадание в корабль противника и выполняет соответствующие действия.
        Возвращает True при попадании, иначе False."""
        for ship in self.ship_manager.ships_copy:
            if shoot in ship:
                ship.remove(shoot)
                self.ship_manager.ships_set.discard(shoot)
                self.injured.add(shoot)
                destroyed = False
                if not ship:
                    destroyed = True
                return True, destroyed

        self.missed.add(shoot)
        return False, False

    @abstractmethod
    def shoot(self, other_player) -> bool:
        """Обрабатывает события мыши для игрового поля и определяет, чей сейчас ход.
               В зависимости от событий, она обновляет состояние игры"""
