"""Функции связанные с процессом выстрела"""
import random
import pygame
from dotted_and_hit import update_dotted_and_hit
import global_variables as my_space
from drawer import Drawer


def random_shot(set_to_shot: set) -> bool:
    """
    Случайным образом выбирает блок из доступных для стрельбы из набора и возвращает hit_or_miss
    """
    pygame.time.delay(my_space.MAX_DELAY_FOR_COMPUTER_SHOT)
    computer_fired = random.choice(tuple(set_to_shot))
    my_space.available_to_fire_set.discard(computer_fired)
    return check_is_successful_hit(computer_fired, my_space.HUMAN_SHIPS, True)


def update_around_comp_hit(shot_coordinates: tuple, computer_hits: bool = True) -> None:
    """
    Обновляет набор блоков вокруг последнего поражения компьютера, удаляя блоки,
    по которым компьютер промахнулся, для эффективного поиска кораблей противника.
    """
    if computer_hits:
        update_around_last_hit(shot_coordinates)
    else:
        remove_from_around_hit_set(shot_coordinates)

    remove_used_blocks_from_around_hit_set()
    update_available_to_fire_set()


def update_around_last_hit(shot_coordinates: tuple) -> None:
    """
    Обновляет множество вокруг последнего поражения компьютера
    """
    if shot_coordinates in my_space.around_hit_set:
        update_around_existing_hit()
    else:
        add_new_around_hit_blocks(shot_coordinates)


def update_around_existing_hit() -> None:
    """
    Обновляет множество вокруг существующего поражения компьютера
    """
    new_hit_set = set()

    for hit_index in range(len(my_space.last_hits) - 1):
        current_hit = my_space.last_hits[hit_index]
        next_hit = my_space.last_hits[hit_index + 1]

        if current_hit[0] == next_hit[0]:  # Если координаты по X одинаковы
            add_around_block(new_hit_set, current_hit[0], current_hit[1] - 1)
            add_around_block(new_hit_set, current_hit[0], next_hit[1] + 1)
        elif current_hit[1] == next_hit[1]:  # Если координаты по Y одинаковы
            add_around_block(new_hit_set, current_hit[0] - 1, current_hit[1])
            add_around_block(new_hit_set, next_hit[0] + 1, current_hit[1])

    my_space.around_hit_set = new_hit_set


def add_around_block(hit_set: set, x_coordinate: int, y_coordinate: int) -> None:
    """
    Добавляет блок вокруг поражения компьютера в множество
    """
    if my_space.MIN_COORDINATE_VALUE < x_coordinate <= my_space.MAX_COORDINATE_VALUE \
            and my_space.MIN_COORDINATE_VALUE < y_coordinate <= my_space.MAX_COORDINATE_VALUE:
        hit_set.add((x_coordinate, y_coordinate))


def add_new_around_hit_blocks(shot_coordinates: tuple) -> None:
    """
    Добавляет новые блоки вокруг последнего поражения компьютера
    """
    x_coordinate, y_coordinate = shot_coordinates
    add_around_block(my_space.around_hit_set, x_coordinate - 1, y_coordinate)
    add_around_block(my_space.around_hit_set, x_coordinate + 1, y_coordinate)
    add_around_block(my_space.around_hit_set, x_coordinate, y_coordinate - 1)
    add_around_block(my_space.around_hit_set, x_coordinate, y_coordinate + 1)


def remove_from_around_hit_set(shot_coordinates: tuple) -> None:
    """
    Удаляет координаты выстрела из множества вокруг поражения компьютера
    """
    my_space.around_hit_set.discard(shot_coordinates)


def remove_used_blocks_from_around_hit_set() -> None:
    """
    Удаляет уже использованные блоки из множества вокруг поражения компьютера
    """
    my_space.around_hit_set -= my_space.dotted_to_shot
    my_space.around_hit_set -= my_space.for_comp_to_shot


def update_available_to_fire_set() -> None:
    """
    Обновляет доступные блоки для стрельбы
    """
    my_space.available_to_fire_set = my_space.available_to_fire_set - my_space.around_hit_set


def check_is_successful_hit(shot_coordinates: tuple[int, int], opponent_ships: list,
                            computer_turn: bool) -> bool:
    """Проверяет попадание в корабль противника и выполняет соответствующие действия.
    Возвращает True при попадании, иначе False."""
    for ship in opponent_ships:
        if shot_coordinates in ship:
            update_dotted_and_hit(shot_coordinates, computer_turn)
            position = opponent_ships.index(ship)
            if len(ship) == 1:
                update_dotted_and_hit(shot_coordinates, computer_turn)
            ship.remove(shot_coordinates)
            if computer_turn:
                my_space.last_hits.append(shot_coordinates)
                my_space.HUMAN.ships_set.discard(shot_coordinates)
                update_around_comp_hit(shot_coordinates)
            else:
                my_space.COMPUTER.ships_set.discard(shot_coordinates)
            if not ship:
                Drawer.process_destroyed_ship(position, opponent_ships, computer_turn)
                if computer_turn:
                    my_space.last_hits.clear()
                    my_space.around_hit_set.clear()
                else:
                    my_space.destroyed_ships.append(
                        my_space.COMPUTER.ships[position])
            return True
    if not computer_turn:
        my_space.dotted.add(shot_coordinates)
    else:
        my_space.dotted.add((shot_coordinates[0] + 15, shot_coordinates[1]))
        my_space.dotted_to_shot.add(shot_coordinates)
    if computer_turn:
        update_around_comp_hit(shot_coordinates, False)
    return False
