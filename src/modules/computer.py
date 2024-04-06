"""В этом модуле реализуется ComputerPlayer и вспомогательные для неё функции и процедуры"""
import random
from typing import Set, Tuple

import pygame
from src.modules.player_class import Player
import src.global_variables as my_space
from src.GUI.gui_drawer import Point


class ComputerPlayer(Player):
    """Реализуем ComputerPlayer"""

    def __init__(self, name: str, offset: int):
        super().__init__(name, offset)
        self.need_to_fire = set[Point]()
        self.to_shot = set[Point]()
        self.horizontal = -1
        self.last_hits = list[Point]()
        self.dotted_to_shot = set[Point]()
        self.available_to_fire_set = set[Point](
            Point(a, b) for a in range(1, my_space.GRID_LIMIT) for b in
            range(1, my_space.GRID_LIMIT))
        # print(sorted(self.available_to_fire_set), sep="\n")

    def update_dotted_and_hit(self, shot_coordinates: Point,
                              diagonal_only: bool) -> None:
        """Эта процедура добавляет точки вокруг клетки, в которую был произведен выстрел"""
        fire_x_coordinate, fire_y_coordinate = shot_coordinates
        min_x, max_x = my_space.DISTANCE, my_space.DISTANCE + my_space.GRID_LIMIT
        fire_x_coordinate += my_space.DISTANCE
        self.to_shot.add(shot_coordinates)
        self.hit_blocks.add((fire_x_coordinate, fire_y_coordinate))
        for add_x_coordinate in range(-1, 2):
            for add_y_coordinate in range(-1, 2):
                if (not diagonal_only and min_x < fire_x_coordinate + add_x_coordinate < max_x and
                        0 < fire_y_coordinate + add_y_coordinate < my_space.GRID_LIMIT):
                    self.dotted.add((fire_x_coordinate + add_x_coordinate,
                                     fire_y_coordinate + add_y_coordinate))
                    self.dotted_to_shot.add(Point(shot_coordinates[0] + add_x_coordinate,
                                                  fire_y_coordinate + add_y_coordinate))
        self.dotted -= self.hit_blocks

    def shoot(self, other_player: Player, shot_taken: bool) -> Tuple[bool, bool]:
        """Стреляет от имени компьютера"""
        if self.need_to_fire:
            is_hit = self.__random_shoot(self.need_to_fire, other_player)
        else:
            is_hit = self.__random_shoot(self.available_to_fire_set, other_player)
        # print("is hit?", is_hit, self.last_hits, self.need_to_fire)
        # print(len(self.available_to_fire_set))
        return is_hit, True

    def __random_shoot(self, set_to_shot: Set[Point], other_player: Player) -> bool:
        """
        Случайным образом выбирает блок из доступных для стрельбы из набора и возвращает hit_or_miss
        """
        pygame.time.delay(my_space.DELAY_FOR_COMPUTER_SHOT)
        computer_fired = random.choice(list(set_to_shot))
        self.available_to_fire_set.discard(computer_fired)
        print(f"Компьютер решил выстрелить в "
              f"{chr(computer_fired[1] - 1 + ord('A')), computer_fired[0]}")
        return self.__check_is_successful_hit(computer_fired, other_player)

    def __check_is_successful_hit(self, shoot: Point, other_player: Player) -> bool:
        """Проверяет попадание в корабль противника и выполняет соответствующие действия.
        Возвращает True при попадании, иначе False."""
        for ship in other_player.ship_manager.ships_copy:
            if shoot in ship:
                self.update_dotted_and_hit(shoot, True)
                position = other_player.ship_manager.ships_copy.index(ship)
                if len(ship) == 1:
                    self.update_dotted_and_hit(shoot, True)
                ship.remove(shoot)
                self.last_hits.append(shoot)
                other_player.ship_manager.ships_set.discard(shoot)
                update_around_comp_hit(shoot, True, self)
                other_player.injured.add(shoot)
                if not ship:
                    # print("deleting")
                    self.process_destroyed_ship(position, other_player, False)
                    for coordinate in self.dotted:
                        other_player.missed.add(
                            Point(coordinate[0] - my_space.DISTANCE, coordinate[1]))
                    # print(self.dotted)
                    self.last_hits.clear()
                    self.need_to_fire.clear()
                return True

        other_player.missed.add(shoot)
        self.dotted.add((shoot[0] + my_space.DISTANCE, shoot[1]))
        self.dotted_to_shot.add(shoot)
        update_around_comp_hit(shoot, False, self)
        return False


def update_around_comp_hit(shot_coordinates: Point, computer_hits: bool,
                           computer: ComputerPlayer) -> None:
    """
    Обновляет набор блоков вокруг последнего поражения компьютера, удаляя блоки,
    по которым компьютер промахнулся, для эффективного поиска кораблей противника.
    """
    if computer_hits:
        update_around_last_hit(shot_coordinates, computer)
    else:
        remove_from_around_hit_set(shot_coordinates, computer)

    remove_used_blocks_from_around_hit_set(computer)
    update_available_to_fire_set(computer)


def update_around_last_hit(shot_coordinates: Point, computer: ComputerPlayer) -> None:
    """
    Обновляет множество вокруг последнего поражения компьютера
    """
    # print(computer.last_hits, "computer last hits")
    if len(computer.last_hits) > 1:
        update_around_existing_hit(computer)
    else:
        add_new_around_hit_blocks(shot_coordinates, computer)


def update_around_existing_hit(computer: ComputerPlayer) -> None:
    """
    Обновляет множество вокруг существующего поражения компьютера
    """
    new_hit_set = set[Point]()

    for hit_index in range(len(computer.last_hits) - 1):
        current_hit = computer.last_hits[hit_index]
        next_hit = computer.last_hits[hit_index + 1]

        if current_hit[0] == next_hit[0]:
            add_around_block(new_hit_set, current_hit[0], current_hit[1] - 1)
            add_around_block(new_hit_set, current_hit[0], current_hit[1] + 1)
            add_around_block(new_hit_set, current_hit[0], next_hit[1] + 1)
            add_around_block(new_hit_set, current_hit[0], next_hit[1] - 1)
        elif current_hit[1] == next_hit[1]:
            add_around_block(new_hit_set, current_hit[0] - 1, current_hit[1])
            add_around_block(new_hit_set, current_hit[0] + 1, current_hit[1])
            add_around_block(new_hit_set, next_hit[0] + 1, current_hit[1])
            add_around_block(new_hit_set, next_hit[0] - 1, current_hit[1])
    # print(computer.need_to_fire, new_hit_set, "check")
    computer.need_to_fire = new_hit_set


def add_around_block(hit_set: Set[Point], x_coordinate: int, y_coordinate: int) -> None:
    """
    Добавляет блок вокруг поражения компьютера в множество
    """
    if my_space.MIN_COORDINATE_VALUE <= x_coordinate <= my_space.MAX_COORDINATE_VALUE \
            and my_space.MIN_COORDINATE_VALUE <= y_coordinate <= my_space.MAX_COORDINATE_VALUE:
        hit_set.add(Point(x_coordinate, y_coordinate))


def add_new_around_hit_blocks(shot_coordinates: Point, computer: ComputerPlayer) -> None:
    """
    Добавляет новые блоки вокруг последнего поражения компьютера
    """
    x_coordinate, y_coordinate = shot_coordinates
    add_around_block(computer.need_to_fire, x_coordinate - 1, y_coordinate)
    add_around_block(computer.need_to_fire, x_coordinate + 1, y_coordinate)
    add_around_block(computer.need_to_fire, x_coordinate, y_coordinate - 1)
    add_around_block(computer.need_to_fire, x_coordinate, y_coordinate + 1)


def remove_from_around_hit_set(shot_coordinates: Point, computer: ComputerPlayer) -> None:
    """
    Удаляет координаты выстрела из множества вокруг поражения компьютера
    """
    computer.need_to_fire.discard(shot_coordinates)


def remove_used_blocks_from_around_hit_set(computer: ComputerPlayer) -> None:
    """
    Удаляет уже использованные блоки из множества вокруг поражения компьютера
    """
    # print("checking dot", computer.need_to_fire, computer.dotted_to_shot, computer.to_shot)
    computer.need_to_fire -= computer.dotted_to_shot
    computer.need_to_fire -= computer.to_shot


def update_available_to_fire_set(computer: ComputerPlayer) -> None:
    """
    Обновляет доступные блоки для стрельбы
    """
    computer.available_to_fire_set -= computer.dotted_to_shot
    computer.available_to_fire_set -= computer.to_shot
