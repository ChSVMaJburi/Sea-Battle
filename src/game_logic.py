import random
import pygame
from dotted_and_hit import dotted_and_hit
import global_variable as my_space
from drawer import Drawer


def shot(set_to_shot):
    """
    Случайным образом выбирает блок из доступных для стрельбы из набора
    """
    pygame.time.delay(my_space.MAX_DELAY_FOR_COMPUTER_SHOT)
    comp_fired = random.choice(tuple(set_to_shot))
    my_space.ava_to_fire_set.discard(comp_fired)
    return hit_or_miss(comp_fired, my_space.H_ships_w, True)


def update_around_comp_hit(shot_coordinates, computer_hits=True):
    """
    Обновляет набор блоков вокруг последнего поражения компьютера, удаляя блоки,
    по которым компьютер промахнулся, для эффективного поиска кораблей противника.
    """
    if computer_hits and shot_coordinates in my_space.around_hit_set:
        new_hit_set = set()

        def add(x, y):
            new_hit_set.add((x, y))

        for i in range(len(my_space.last_hits) - 1):
            if my_space.last_hits[i][0] == my_space.last_hits[i + 1][0]:
                if my_space.MIN_COORDINATE_VALUE < my_space.last_hits[i][1]:
                    add(my_space.last_hits[i][0],
                        my_space.last_hits[i][1] - 1)
                if my_space.MIN_COORDINATE_VALUE < my_space.last_hits[i + 1][1]:
                    add(my_space.last_hits[i][0],
                        my_space.last_hits[i + 1][1] - 1)
                if my_space.last_hits[i][1] < my_space.MAX_COORDINATE_VALUE:
                    add(my_space.last_hits[i][0],
                        my_space.last_hits[i][1] + 1)
                if my_space.last_hits[i + 1][1] < my_space.MAX_COORDINATE_VALUE:
                    add(my_space.last_hits[i][0],
                        my_space.last_hits[i + 1][1] + 1)
            elif my_space.last_hits[i][1] == my_space.last_hits[i + 1][1]:
                if my_space.MIN_COORDINATE_VALUE < my_space.last_hits[i][0]:
                    add(my_space.last_hits[i][0] -
                        1, my_space.last_hits[i][1])
                if my_space.MIN_COORDINATE_VALUE < my_space.last_hits[i + 1][0]:
                    add(my_space.last_hits[i + 1][0] -
                        1, my_space.last_hits[i][1])
                if my_space.last_hits[i][0] < my_space.MAX_COORDINATE_VALUE:
                    add(my_space.last_hits[i][0] +
                        1, my_space.last_hits[i][1])
                if my_space.last_hits[i + 1][0] < my_space.MAX_COORDINATE_VALUE:
                    add(my_space.last_hits[i + 1][0] +
                        1, my_space.last_hits[i][1])
        my_space.around_hit_set = new_hit_set

    elif computer_hits and shot_coordinates not in my_space.around_hit_set:
        x, y = shot_coordinates
        if my_space.MIN_COORDINATE_VALUE < x:
            my_space.around_hit_set.add((x - 1, y))
        if my_space.MIN_COORDINATE_VALUE < y:
            my_space.around_hit_set.add((x, y - 1))
        if x < my_space.MAX_COORDINATE_VALUE:
            my_space.around_hit_set.add((x + 1, y))
        if y < my_space.MAX_COORDINATE_VALUE:
            my_space.around_hit_set.add((x, y + 1))
    elif not computer_hits:
        my_space.around_hit_set.discard(shot_coordinates)

    my_space.around_hit_set -= my_space.dotted_to_shot
    my_space.around_hit_set -= my_space.for_comp_to_shot
    my_space.ava_to_fire_set -= my_space.around_hit_set
    my_space.ava_to_fire_set -= my_space.dotted_to_shot


def hit_or_miss(shot_coordinates, opponent_ships, comp_turn):
    """
    Проверяет попадание в корабль противника и выполняет соответствующие действия.
    Возвращает True при попадании, иначе False.
    """
    for i in opponent_ships:
        if shot_coordinates in i:
            dotted_and_hit(
                shot_coordinates, comp_turn)
            pos = opponent_ships.index(i)
            if len(i) == 1:
                dotted_and_hit(shot_coordinates, comp_turn)
            i.remove(shot_coordinates)
            if comp_turn:
                my_space.last_hits.append(shot_coordinates)
                my_space.human.ships_set.discard(shot_coordinates)
                update_around_comp_hit(shot_coordinates)
            else:
                my_space.computer.ships_set.discard(shot_coordinates)
            if not i:
                Drawer.destroyed_ships(pos, opponent_ships, comp_turn)
                if comp_turn:
                    my_space.last_hits.clear()
                    my_space.around_hit_set.clear()
                else:
                    my_space.destroyed_ships.append(
                        my_space.computer.ships[pos])
            return True
    if not comp_turn:
        my_space.dotted.add(shot_coordinates)
    else:
        my_space.dotted.add((shot_coordinates[0] + 15, shot_coordinates[1]))
        my_space.dotted_to_shot.add(shot_coordinates)
    if comp_turn:
        update_around_comp_hit(shot_coordinates, False)
    return False
