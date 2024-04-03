import random
import pygame
from dotted_and_hit import dotted_and_hit
import const_variable as const
from drawer import Drawer


def shot(set_to_shot):
    """
    Случайным образом выбирает блок из доступных для стрельбы из набора
    """
    pygame.time.delay(const.MAX_DELAY_FOR_COMPUTER_SHOT)
    comp_fired = random.choice(tuple(set_to_shot))
    const.available_to_fire_set.discard(comp_fired)
    return hit_or_miss(comp_fired, const.HUMAN_SHIPS, True)


def update_around_comp_hit(shot_coordinates, computer_hits=True):
    """
    Обновляет набор блоков вокруг последнего поражения компьютера, удаляя блоки,
    по которым компьютер промахнулся, для эффективного поиска кораблей противника.
    """
    if computer_hits and shot_coordinates in const.around_hit_set:
        new_hit_set = set()

        def add(x, y):
            new_hit_set.add((x, y))

        for i in range(len(const.last_hits) - 1):
            if const.last_hits[i][0] == const.last_hits[i + 1][0]:
                if const.MIN_COORDINATE_VALUE < const.last_hits[i][1]:
                    add(const.last_hits[i][0],
                        const.last_hits[i][1] - 1)
                if const.MIN_COORDINATE_VALUE < const.last_hits[i + 1][1]:
                    add(const.last_hits[i][0],
                        const.last_hits[i + 1][1] - 1)
                if const.last_hits[i][1] < const.MAX_COORDINATE_VALUE:
                    add(const.last_hits[i][0],
                        const.last_hits[i][1] + 1)
                if const.last_hits[i + 1][1] < const.MAX_COORDINATE_VALUE:
                    add(const.last_hits[i][0],
                        const.last_hits[i + 1][1] + 1)
            elif const.last_hits[i][1] == const.last_hits[i + 1][1]:
                if const.MIN_COORDINATE_VALUE < const.last_hits[i][0]:
                    add(const.last_hits[i][0] -
                        1, const.last_hits[i][1])
                if const.MIN_COORDINATE_VALUE < const.last_hits[i + 1][0]:
                    add(const.last_hits[i + 1][0] -
                        1, const.last_hits[i][1])
                if const.last_hits[i][0] < const.MAX_COORDINATE_VALUE:
                    add(const.last_hits[i][0] +
                        1, const.last_hits[i][1])
                if const.last_hits[i + 1][0] < const.MAX_COORDINATE_VALUE:
                    add(const.last_hits[i + 1][0] +
                        1, const.last_hits[i][1])
        const.around_hit_set = new_hit_set

    elif computer_hits and shot_coordinates not in const.around_hit_set:
        x, y = shot_coordinates
        if const.MIN_COORDINATE_VALUE < x:
            const.around_hit_set.add((x - 1, y))
        if const.MIN_COORDINATE_VALUE < y:
            const.around_hit_set.add((x, y - 1))
        if x < const.MAX_COORDINATE_VALUE:
            const.around_hit_set.add((x + 1, y))
        if y < const.MAX_COORDINATE_VALUE:
            const.around_hit_set.add((x, y + 1))
    elif not computer_hits:
        const.around_hit_set.discard(shot_coordinates)

    const.around_hit_set -= const.dotted_to_shot
    const.around_hit_set -= const.for_comp_to_shot
    const.available_to_fire_set -= const.around_hit_set
    const.available_to_fire_set -= const.dotted_to_shot


def hit_or_miss(shot_coordinates, opponent_ships, computer_turn):
    """
    Проверяет попадание в корабль противника и выполняет соответствующие действия.
    Возвращает True при попадании, иначе False.
    """
    for i in opponent_ships:
        if shot_coordinates in i:
            dotted_and_hit(
                shot_coordinates, computer_turn)
            pos = opponent_ships.index(i)
            if len(i) == 1:
                dotted_and_hit(shot_coordinates, computer_turn)
            i.remove(shot_coordinates)
            if computer_turn:
                const.last_hits.append(shot_coordinates)
                const.HUMAN.ships_set.discard(shot_coordinates)
                update_around_comp_hit(shot_coordinates)
            else:
                const.COMPUTER.ships_set.discard(shot_coordinates)
            if not i:
                Drawer.destroyed_ships(pos, opponent_ships, computer_turn)
                if computer_turn:
                    const.last_hits.clear()
                    const.around_hit_set.clear()
                else:
                    const.destroyed_ships.append(
                        const.COMPUTER.ships[pos])
            return True
    if not computer_turn:
        const.dotted.add(shot_coordinates)
    else:
        const.dotted.add((shot_coordinates[0] + 15, shot_coordinates[1]))
        const.dotted_to_shot.add(shot_coordinates)
    if computer_turn:
        update_around_comp_hit(shot_coordinates, False)
    return False
