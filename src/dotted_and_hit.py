from typing import Tuple
import const_variable as const


def dotted_and_hit(shot_coordinates: Tuple[int, int], computer_turn: bool, diagonal_only: bool = True) -> None:
    """"""
    fire_x, fire_y = shot_coordinates
    min_x, max_x = 0, const.GRID_LIMIT
    if computer_turn:
        fire_x += const.MAX_X_OFFSET
        min_x += const.MAX_X_OFFSET
        max_x += const.MAX_X_OFFSET
        const.for_comp_to_shot.add(shot_coordinates)
    const.hit_blocks.add((fire_x, fire_y))
    for i in range(-1, 2):
        for j in range(-1, 2):
            if not diagonal_only and min_x < fire_x + i < max_x and 0 < fire_y + j < 11:
                const.dotted.add((fire_x + i, fire_y + j))
                if computer_turn:
                    const.dotted_to_shot.add((shot_coordinates[0] + i, fire_y + j))
    const.dotted -= const.hit_blocks
