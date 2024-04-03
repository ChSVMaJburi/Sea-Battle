from button import Button
import const_variables as const
from drawer import Drawer
from grid_class import Grid
import copy
from drawer import ShipDrawer

import pygame
import game_logic as logic

pygame.init()

st_game = const.LEFT_MARGIN + const.GRID_SIZE * const.BLOCK_SIZE
st_button = Button(st_game, "START GAME")


def display_the_start_screen(game_over):
    flag = True
    while flag:
        st_button.draw_button()
        st_button.change_color_on_hover()
        pygame.display.update()
        m = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                flag = False
                game_over = True
            elif event.type == pygame.MOUSEBUTTONDOWN and st_button.rect.collidepoint(m):
                flag = False
        pygame.display.update()
        const.screen.fill(const.BLUE,
                          (const.RECTANGLE_X, const.RECTANGLE_Y, const.RECTANGLE_WIDTH,
                           const.RECTANGLE_HEIGHT))
    return flag, game_over


def gameplay(game_over: bool, computer_turn: bool, flag: bool):
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            game_over = True
        elif not computer_turn and i.type == pygame.MOUSEBUTTONDOWN:
            x, y = i.pos
            if const.MIN_X <= x <= const.MAX_X and const.MIN_Y <= y <= const.MAX_Y:
                if (
                        const.LEFT_MARGIN < x < const.LEFT_MARGIN + const.GRID_OFFSET * const.BLOCK_SIZE) and (
                        const.UP_MARGIN < y < const.UP_MARGIN + const.GRID_OFFSET * const.BLOCK_SIZE):
                    flag = False
                    shot_coordinates = ((x - const.LEFT_MARGIN) // const.BLOCK_SIZE + 1,
                                        (y - const.UP_MARGIN) // const.BLOCK_SIZE + 1)
                    for i in const.hit_blocks:
                        if i == shot_coordinates:
                            flag = True

                    for i in const.dotted:
                        if i == shot_coordinates:
                            flag = True
                if flag == False:
                    computer_turn = not logic.hit_or_miss(
                        shot_coordinates, const.COMPUTER_SHIPS, computer_turn)

    if computer_turn:
        if const.around_hit_set:
            computer_turn = logic.shot(const.around_hit_set)
        else:
            computer_turn = logic.shot(const.available_to_fire_set)
    return game_over, computer_turn, flag


def init_pygame():
    """Проделаем стартовые операции pygame"""
    const.HUMAN = ShipDrawer()
    const.HUMAN_SHIPS = copy.deepcopy(const.HUMAN.ships)
    const.COMPUTER = ShipDrawer()
    const.COMPUTER_SHIPS = copy.deepcopy(const.COMPUTER.ships)
    const.screen.fill(const.BLUE)


def play():
    init_pygame()
    Grid("COMPUTER", 0)
    Grid("HUMAN", const.DISTANCE)
    Drawer.ship(const.HUMAN.ships)
    computer_turn = False
    flag, game_over = display_the_start_screen(False)
    while not game_over:
        game_over, computer_turn, flag = gameplay(game_over, computer_turn, flag)
        Drawer.dotted(const.dotted)
        Drawer.hit_blocks(const.hit_blocks)
        Drawer.ship(const.destroyed_ships)
        if not const.COMPUTER.ships_set:
            show_mess(
                "YOU WIN!", (0, 0, const.SIZE[0], const.SIZE[1]), const.GAME_OVER)
        if not const.HUMAN.ships_set:
            show_mess(
                "YOU LOSE!", (0, 0, const.SIZE[0], const.SIZE[1]), const.GAME_OVER)
            Drawer.ship(const.COMPUTER.ships)
        pygame.display.update()
    pygame.quit()


def show_mess(mess: str, rectangle: tuple, w_f=const.font):
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
    backgr_r = pygame.Rect(x - const.BLOCK_SIZE / 2,
                           y, mess_w + const.BLOCK_SIZE, mess_h)
    mess_blit = w_f.render(mess, True, const.RED)
    const.screen.fill(const.BLUE, backgr_r)
    const.screen.blit(mess_blit, (x, y))
