from typing import Tuple
import global_variable as my_space


def dotted_and_hit(shot_coordinates: Tuple[int, int], comp_turn: bool, diagonal_only: bool = True) -> None:
    fire_x, fire_y = shot_coordinates
    min_x, max_x = 0, my_space.GRID_LIMIT
    if comp_turn:
        fire_x += my_space.MAX_X_OFFSET
        min_x += my_space.MAX_X_OFFSET
        max_x += my_space.MAX_X_OFFSET
        my_space.for_comp_to_shot.add(shot_coordinates)
    my_space.hit_Bl.add((fire_x, fire_y))
    for i in range(-1, 2):
        for j in range(-1, 2):
            if not diagonal_only and min_x < fire_x + i < max_x and 0 < fire_y + j < 11:
                my_space.dotted.add((fire_x + i, fire_y + j))
                if comp_turn:
                    my_space.dotted_to_shot.add((shot_coordinates[0] + i, fire_y + j))
    my_space.dotted -= my_space.hit_Bl
