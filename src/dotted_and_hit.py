"""Реализуем процедуру update_dotted_and_hit"""
from typing import Tuple
import const_variables as const


def update_dotted_and_hit(shot_coordinates: Tuple[int, int], computer_turn: bool,
                          diagonal_only: bool = True) -> None:
    """Эта процедура добавляет точки вокруг клетки, в которую был произведен выстрел"""
    fire_x_coordinate, fire_y_coordinate = shot_coordinates
    min_x, max_x = 0, const.GRID_LIMIT
    if computer_turn:
        fire_x_coordinate += const.MAX_X_OFFSET
        min_x += const.MAX_X_OFFSET
        max_x += const.MAX_X_OFFSET
        const.for_comp_to_shot.add(shot_coordinates)
    const.hit_blocks.add((fire_x_coordinate, fire_y_coordinate))
    for add_x_coordinate in range(-1, 2):
        for add_y_coordinate in range(-1, 2):
            if (not diagonal_only and min_x < fire_x_coordinate + add_x_coordinate < max_x and
                    0 < fire_y_coordinate + add_y_coordinate < const.GRID_LIMIT):
                const.dotted.add(
                    (fire_x_coordinate + add_x_coordinate, fire_y_coordinate + add_y_coordinate))
                if computer_turn:
                    const.dotted_to_shot.add((shot_coordinates[0] + add_x_coordinate,
                                              fire_y_coordinate + add_y_coordinate))
    const.dotted -= const.hit_blocks
