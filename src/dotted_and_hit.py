import pygame
from typing import Tuple
import global_variable as glob


def dotted_and_hit(shot_coordinates: Tuple[int, int], comp_turn: bool, diagonal_only: bool = True) -> None:
    fire_x, fire_y = shot_coordinates
    min_x, max_x = 0, glob.GRID_LIMIT
    if comp_turn:
        fire_x += glob.MAX_X_OFFSET
        min_x += glob.MAX_X_OFFSET
        max_x += glob.MAX_X_OFFSET
        glob.for_comp_to_shot.add(shot_coordinates)
    glob.hit_Bl.add((fire_x, fire_y))
    for i in range(-1, 2):
        for j in range(-1, 2):
            if not diagonal_only and min_x < fire_x + i < max_x and 0 < fire_y + j < 11:
                glob.dotted.add((fire_x + i, fire_y + j))
                if comp_turn:
                    glob.dotted_to_shot.add((shot_coordinates[0] + i, fire_y + j))
    glob.dotted -= glob.hit_Bl
