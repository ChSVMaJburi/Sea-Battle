"""Функции связанные с процессом выстрела"""
import global_variables as my_space
from players import Player


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


def update_around_last_hit(shot_coordinates: tuple, player: Player) -> None:
    """
    Обновляет множество вокруг последнего поражения компьютера
    """
    if shot_coordinates in player.drawer.ships_set:
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

    my_space.izmeni_shahrom = new_hit_set


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
    add_around_block(my_space.izmeni_shahrom, x_coordinate - 1, y_coordinate)
    add_around_block(my_space.izmeni_shahrom, x_coordinate + 1, y_coordinate)
    add_around_block(my_space.izmeni_shahrom, x_coordinate, y_coordinate - 1)
    add_around_block(my_space.izmeni_shahrom, x_coordinate, y_coordinate + 1)


def remove_from_around_hit_set(shot_coordinates: tuple) -> None:
    """
    Удаляет координаты выстрела из множества вокруг поражения компьютера
    """
    my_space.izmeni_shahrom.discard(shot_coordinates)


def remove_used_blocks_from_around_hit_set() -> None:
    """
    Удаляет уже использованные блоки из множества вокруг поражения компьютера
    """
    my_space.izmeni_shahrom -= my_space.dotted_to_shot
    my_space.izmeni_shahrom -= my_space.nado_ubrat_for_comp_to_shot


def update_available_to_fire_set() -> None:
    """
    Обновляет доступные блоки для стрельбы
    """
    my_space.available_to_fire_set = my_space.available_to_fire_set - my_space.izmeni_shahrom
