from button import button
import global_variable as variables
from draw import draw
from Grid import Grid
from dotted_and_hit import dotted_and_hit
import random
import pygame

pygame.init()

st_game = variables.l_margin + 10 * variables.block_sz
st_button = button(st_game, "START GAME")


def hit_or_miss(fired_BL, oppo_ships_list, comp_turn):
    """
    Проверяет, является ли блок, в коsudo pip3 install pygameторый был произведен выстрел компьютером или человеком, попаданием или промахом.
    Обновляет наборы с помощью точек.
    Удаляет уничтоженные корабли из списка кораблей.
    """
    for i in oppo_ships_list:
        if fired_BL in i:
            dotted_and_hit(
                fired_BL, comp_turn)
            pos = oppo_ships_list.index(i)
            if len(i) == 1:
                dotted_and_hit(fired_BL, comp_turn)
            i.remove(fired_BL)
            if comp_turn:
                variables.last_hits.append(fired_BL)
                variables.human.ships_set.discard(fired_BL)
                update_around_comp_hit(fired_BL)
            else:
                variables.computer.ships_set.discard(fired_BL)
            if not i:
                draw.destroyed_ships(pos, oppo_ships_list, comp_turn)
                if comp_turn:
                    variables.last_hits.clear()
                    variables.around_hit_set.clear()
                else:
                    variables.destroyed_ships.append(
                        variables.computer.ships[pos])
            return True
    if not comp_turn:
        variables.dotted.add(fired_BL)
    else:
        variables.dotted.add((fired_BL[0] + 15, fired_BL[1]))
        variables.dotted_to_shoot.add(fired_BL)
    if comp_turn:
        update_around_comp_hit(fired_BL, False)
    return False


def shoot(set_to_shoot):
    """
    Случайным образом выбирает блок из доступных для стрельбы из набора
    """
    pygame.time.delay(700)
    comp_fired = random.choice(tuple(set_to_shoot))
    variables.ava_to_fire_set.discard(comp_fired)
    return hit_or_miss(comp_fired, variables.H_ships_w, True)


def update_around_comp_hit(fired_BL, computer_hits=True):
    """
    Обновляет around_last_computer_hit_set. Добавляет к этому набору вертикальные или горизонтальные блоки вокруг
    блока, который был поражен последним. Затем удаляет те блоки из этого набора, в которые стреляли, но промахнулись.
    around_last_computer_hit_set заставляет компьютер выбирать правильные блоки, чтобы быстро уничтожить корабль
    , вместо того, чтобы просто случайным образом стрелять по совершенно случайным блокам.
    """
    if computer_hits and fired_BL in variables.around_hit_set:
        new_hit_set = set()

        def add(x, y):
            new_hit_set.add((x, y))

        for i in range(len(variables.last_hits) - 1):
            if variables.last_hits[i][0] == variables.last_hits[i + 1][0]:
                if 1 < variables.last_hits[i][1]:
                    add(variables.last_hits[i][0],
                        variables.last_hits[i][1] - 1)
                if 1 < variables.last_hits[i + 1][1]:
                    add(variables.last_hits[i][0],
                        variables.last_hits[i + 1][1] - 1)
                if variables.last_hits[i][1] < 10:
                    add(variables.last_hits[i][0],
                        variables.last_hits[i][1] + 1)
                if variables.last_hits[i + 1][1] < 10:
                    add(variables.last_hits[i][0],
                        variables.last_hits[i + 1][1] + 1)
            elif variables.last_hits[i][1] == variables.last_hits[i + 1][1]:
                if 1 < variables.last_hits[i][0]:
                    add(variables.last_hits[i][0] -
                        1, variables.last_hits[i][1])
                if 1 < variables.last_hits[i + 1][0]:
                    add(variables.last_hits[i + 1][0] -
                        1, variables.last_hits[i][1])
                if variables.last_hits[i][0] < 10:
                    add(variables.last_hits[i][0] +
                        1, variables.last_hits[i][1])
                if variables.last_hits[i + 1][0] < 10:
                    add(variables.last_hits[i + 1][0] +
                        1, variables.last_hits[i][1])
        variables.around_hit_set = new_hit_set

    elif computer_hits and fired_BL not in variables.around_hit_set:
        x, y = fired_BL
        if 1 < x:
            variables.around_hit_set.add((x - 1, y))
        if 1 < y:
            variables.around_hit_set.add((x, y - 1))
        if x < 10:
            variables.around_hit_set.add((x + 1, y))
        if y < 10:
            variables.around_hit_set.add((x, y + 1))
    elif not computer_hits:
        variables.around_hit_set.discard(fired_BL)

    variables.around_hit_set -= variables.dotted_to_shoot
    variables.around_hit_set -= variables.for_comp_to_shoot
    variables.ava_to_fire_set -= variables.around_hit_set
    variables.ava_to_fire_set -= variables.dotted_to_shoot


def show_mess(mess, r, w_f=variables.font):
    """
    Выводит сообщение на экран в центре заданного прямоугольника.
    Аргументы:
        mess (str): Сообщение для печати
        r (tuple): прямоугольник в формате
        w_f (объект шрифта pygame): Какой шрифт использовать для печати сообщения. По умолчанию используется шрифт.
    """
    mess_w, mess_h = w_f.size(mess)
    mess_r = pygame.Rect(r)
    x = mess_r.centerx - mess_w / 2
    y = mess_r.centery - mess_h / 2
    backgr_r = pygame.Rect(x - variables.block_sz / 2,
                           y, mess_w + variables.block_sz, mess_h)
    mess_blit = w_f.render(mess, True, variables.RED)
    variables.screen.fill(variables.BLUE, backgr_r)
    variables.screen.blit(mess_blit, (x, y))


def main():
    variables.screen.fill(variables.BLUE)
    f = True
    Grid("COMPUTER", 0)
    Grid("HUMAN", 15)
    draw.ship(variables.human.ships)
    rect_button = (650, 352, 194, 72)
    game_over = False
    comp_turn = False
    while f:
        st_button.Draw()
        st_button.change_cl()
        pygame.display.update()
        m = pygame.mouse.get_pos()
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                f = False
            elif i.type == pygame.MOUSEBUTTONDOWN and st_button.rect.collidepoint(m):
                f = False
        pygame.display.update()
        variables.screen.fill(variables.BLUE, (650, 332, 154, 72))

    while not game_over:
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                game_over = True
            elif not comp_turn and i.type == pygame.MOUSEBUTTONDOWN:
                x, y = i.pos
                if 100 <= x <= 600 and 80 <= y <= 580:
                    if (variables.l_margin < x < variables.l_margin + 10 * variables.block_sz) and (
                            variables.upp_margin < y < variables.upp_margin + 10 * variables.block_sz):
                        f = 0
                        fired_BL = ((x - variables.l_margin) // variables.block_sz + 1,
                                    (y - variables.upp_margin) // variables.block_sz + 1)
                        for i in variables.hit_Bl:
                            if i == fired_BL:
                                f = 1

                        for i in variables.dotted:
                            if i == fired_BL:
                                f = 1
                    if f == 0:
                        comp_turn = not hit_or_miss(
                            fired_BL, variables.ship_w, comp_turn)

        if comp_turn:
            if variables.around_hit_set:
                comp_turn = shoot(variables.around_hit_set)
            else:
                comp_turn = shoot(variables.ava_to_fire_set)

        draw.dotted(variables.dotted)
        draw.hit_Bl(variables.hit_Bl)
        draw.ship(variables.destroyed_ships)
        if not variables.computer.ships_set:
            show_mess(
                "YOU WIN!", (0, 0, variables.size[0], variables.size[1]), variables.gameover_f)
        if not variables.human.ships_set:
            show_mess(
                "YOU LOSE!", (0, 0, variables.size[0], variables.size[1]), variables.gameover_f)
            draw.ship(variables.computer.ships)
        pygame.display.update()


main()
pygame.quit()
