from button import Button
import global_variable as my_space
from drawer import Drawer
from Grid import Grid
import copy
from drawer import ShipDrawer

import pygame
import game_logic as logic

pygame.init()

st_game = my_space.LEFT_MARGIN + my_space.GRID_SIZE * my_space.BLOCK_SIZE
st_button = Button(st_game, "START GAME")


def display_the_start_screen():
    flag = True
    while flag:
        st_button.draw_button()
        st_button.change_color_on_hover()
        pygame.display.update()
        m = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                flag = False
            elif event.type == pygame.MOUSEBUTTONDOWN and st_button.rect.collidepoint(m):
                flag = False
        pygame.display.update()
        my_space.screen.fill(my_space.BLUE,
                             (my_space.RECTANGLE_X, my_space.RECTANGLE_Y, my_space.RECTANGLE_WIDTH,
                              my_space.RECTANGLE_HEIGHT))
    return flag


def gameplay(game_over: bool, comp_turn: bool, flag: bool):
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            game_over = True
        elif not comp_turn and i.type == pygame.MOUSEBUTTONDOWN:
            x, y = i.pos
            if my_space.MIN_X <= x <= my_space.MAX_X and my_space.MIN_Y <= y <= my_space.MAX_Y:
                if (my_space.LEFT_MARGIN < x < my_space.LEFT_MARGIN + my_space.GRID_OFFSET * my_space.BLOCK_SIZE) and (
                        my_space.UP_MARGIN < y < my_space.UP_MARGIN + my_space.GRID_OFFSET * my_space.BLOCK_SIZE):
                    flag = 0
                    shot_coordinates = ((x - my_space.LEFT_MARGIN) // my_space.BLOCK_SIZE + 1,
                                        (y - my_space.UP_MARGIN) // my_space.BLOCK_SIZE + 1)
                    for i in my_space.hit_blocks:
                        if i == shot_coordinates:
                            flag = 1

                    for i in my_space.dotted:
                        if i == shot_coordinates:
                            flag = 1
                if flag == 0:
                    comp_turn = not logic.hit_or_miss(
                        shot_coordinates, my_space.computer_ships, comp_turn)

    if comp_turn:
        if my_space.around_hit_set:
            comp_turn = logic.shot(my_space.around_hit_set)
        else:
            comp_turn = logic.shot(my_space.available_to_fire_set)
    return game_over, comp_turn, flag


def play():
    my_space.human = ShipDrawer()
    my_space.human_ships = copy.deepcopy(my_space.human.ships)
    my_space.computer = ShipDrawer()
    my_space.computer_ships = copy.deepcopy(my_space.computer.ships)
    my_space.screen.fill(my_space.BLUE)
    Grid("COMPUTER", 0)
    Grid("HUMAN", my_space.DISTANCE)
    Drawer.ship(my_space.human.ships)
    game_over = False
    comp_turn = False
    flag = display_the_start_screen()
    while not game_over:
        game_over, comp_turn, flag = gameplay(game_over, comp_turn, flag)
        Drawer.dotted(my_space.dotted)
        Drawer.hit_blocks(my_space.hit_blocks)
        Drawer.ship(my_space.destroyed_ships)
        if not my_space.computer.ships_set:
            show_mess(
                "YOU WIN!", (0, 0, my_space.SIZE[0], my_space.SIZE[1]), my_space.GAME_OVER)
        if not my_space.human.ships_set:
            show_mess(
                "YOU LOSE!", (0, 0, my_space.SIZE[0], my_space.SIZE[1]), my_space.GAME_OVER)
            Drawer.ship(my_space.computer.ships)
        pygame.display.update()


def show_mess(mess: str, rectangle: tuple, w_f=my_space.font):
    """
    Выводит сообщение на экран в центре заданного прямоугольника.
    Аргументы:
        mess (str): Сообщение для печати
        r (tuple): прямоугольник в формате
        w_f (объект шрифта pygame): Какой шрифт использовать для печати сообщения. По умолчанию используется шрифт.
    """
    mess_w, mess_h = w_f.size(mess)
    mess_r = pygame.Rect(rectangle)
    x = mess_r.centerx - mess_w / 2
    y = mess_r.centery - mess_h / 2
    backgr_r = pygame.Rect(x - my_space.BLOCK_SIZE / 2,
                           y, mess_w + my_space.BLOCK_SIZE, mess_h)
    mess_blit = w_f.render(mess, True, my_space.RED)
    my_space.screen.fill(my_space.BLUE, backgr_r)
    my_space.screen.blit(mess_blit, (x, y))
