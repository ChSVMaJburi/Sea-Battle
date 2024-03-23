import random
import pygame
from dotted_and_hit import dotted_and_hit
import global_variable as glob
from drawer import Drawer


def shot(set_to_shot):
    """
    Случайным образом выбирает блок из доступных для стрельбы из набора
    """
    pygame.time.delay(glob.MAX_DELAY_FOR_COMPUTER_SHOT)
    comp_fired = random.choice(tuple(set_to_shot))
    glob.ava_to_fire_set.discard(comp_fired)
    return hit_or_miss(comp_fired, glob.H_ships_w, True)


def update_around_comp_hit(shot_coordinates, computer_hits=True):
    """
    Обновляет набор блоков вокруг последнего поражения компьютера, удаляя блоки,
    по которым компьютер промахнулся, для эффективного поиска кораблей противника.
    """
    if computer_hits and shot_coordinates in glob.around_hit_set:
        new_hit_set = set()

        def add(x, y):
            new_hit_set.add((x, y))

        for i in range(len(glob.last_hits) - 1):
            if glob.last_hits[i][0] == glob.last_hits[i + 1][0]:
                if glob.MIN_COORDINATE_VALUE < glob.last_hits[i][1]:
                    add(glob.last_hits[i][0],
                        glob.last_hits[i][1] - 1)
                if glob.MIN_COORDINATE_VALUE < glob.last_hits[i + 1][1]:
                    add(glob.last_hits[i][0],
                        glob.last_hits[i + 1][1] - 1)
                if glob.last_hits[i][1] < glob.MAX_COORDINATE_VALUE:
                    add(glob.last_hits[i][0],
                        glob.last_hits[i][1] + 1)
                if glob.last_hits[i + 1][1] < glob.MAX_COORDINATE_VALUE:
                    add(glob.last_hits[i][0],
                        glob.last_hits[i + 1][1] + 1)
            elif glob.last_hits[i][1] == glob.last_hits[i + 1][1]:
                if glob.MIN_COORDINATE_VALUE < glob.last_hits[i][0]:
                    add(glob.last_hits[i][0] -
                        1, glob.last_hits[i][1])
                if glob.MIN_COORDINATE_VALUE < glob.last_hits[i + 1][0]:
                    add(glob.last_hits[i + 1][0] -
                        1, glob.last_hits[i][1])
                if glob.last_hits[i][0] < glob.MAX_COORDINATE_VALUE:
                    add(glob.last_hits[i][0] +
                        1, glob.last_hits[i][1])
                if glob.last_hits[i + 1][0] < glob.MAX_COORDINATE_VALUE:
                    add(glob.last_hits[i + 1][0] +
                        1, glob.last_hits[i][1])
        glob.around_hit_set = new_hit_set

    elif computer_hits and shot_coordinates not in glob.around_hit_set:
        x, y = shot_coordinates
        if glob.MIN_COORDINATE_VALUE < x:
            glob.around_hit_set.add((x - 1, y))
        if glob.MIN_COORDINATE_VALUE < y:
            glob.around_hit_set.add((x, y - 1))
        if x < glob.MAX_COORDINATE_VALUE:
            glob.around_hit_set.add((x + 1, y))
        if y < glob.MAX_COORDINATE_VALUE:
            glob.around_hit_set.add((x, y + 1))
    elif not computer_hits:
        glob.around_hit_set.discard(shot_coordinates)

    glob.around_hit_set -= glob.dotted_to_shot
    glob.around_hit_set -= glob.for_comp_to_shot
    glob.ava_to_fire_set -= glob.around_hit_set
    glob.ava_to_fire_set -= glob.dotted_to_shot


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
                glob.last_hits.append(shot_coordinates)
                glob.human.ships_set.discard(shot_coordinates)
                update_around_comp_hit(shot_coordinates)
            else:
                glob.computer.ships_set.discard(shot_coordinates)
            if not i:
                Drawer.destroyed_ships(pos, opponent_ships, comp_turn)
                if comp_turn:
                    glob.last_hits.clear()
                    glob.around_hit_set.clear()
                else:
                    glob.destroyed_ships.append(
                        glob.computer.ships[pos])
            return True
    if not comp_turn:
        glob.dotted.add(shot_coordinates)
    else:
        glob.dotted.add((shot_coordinates[0] + 15, shot_coordinates[1]))
        glob.dotted_to_shot.add(shot_coordinates)
    if comp_turn:
        update_around_comp_hit(shot_coordinates, False)
    return False
