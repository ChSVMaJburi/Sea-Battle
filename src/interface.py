import copy
import pygame
from button import Button
import const_variables as const
from grid_class import Grid
from drawer import Drawer, ShipDrawer

import game_logic as logic

pygame.init()

start_game_x_position = const.LEFT_MARGIN + const.GRID_SIZE * const.BLOCK_SIZE
start_button = Button(start_game_x_position, "START GAME")


def display_the_start_screen(game_over: bool) -> tuple[bool, bool]:
    """"Создает кнопку "START GAME", рисует ее на экране и обрабатывает события мыши"""
    flag = True
    while flag:
        start_button.draw_button()
        start_button.change_color_on_hover()
        pygame.display.update()
        mouse_position = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                flag = False
                game_over = True
            elif (event.type == pygame.MOUSEBUTTONDOWN and
                  start_button.rect.collidepoint(mouse_position)):
                flag = False
        pygame.display.update()
        const.screen.fill(const.BLUE,
                          (const.RECTANGLE_X, const.RECTANGLE_Y, const.RECTANGLE_WIDTH,
                           const.RECTANGLE_HEIGHT))
    return flag, game_over


def handle_mouse_event(event):
    """Обрабатывает события мыши для хода игрока."""
    if event.type == pygame.MOUSEBUTTONDOWN:
        x_coordinate, y_coordinate = event.pos
        if (const.MIN_X <= x_coordinate <= const.MAX_X and
                const.MIN_Y <= y_coordinate <= const.MAX_Y):
            if ((const.LEFT_MARGIN < x_coordinate < const.LEFT_MARGIN +
                 const.GRID_OFFSET * const.BLOCK_SIZE) and
                    (const.UP_MARGIN < y_coordinate < const.UP_MARGIN +
                     const.GRID_OFFSET * const.BLOCK_SIZE)):
                return ((x_coordinate - const.LEFT_MARGIN) // const.BLOCK_SIZE + 1,
                        (y_coordinate - const.UP_MARGIN) // const.BLOCK_SIZE + 1)
    return None


def gameplay(game_over: bool, computer_turn: bool, flag: bool) -> tuple[bool, bool, bool]:
    """Обрабатывает события мыши для игрового поля и определяет, чей сейчас ход.
       В зависимости от событий, она обновляет состояние игры"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True, computer_turn, flag  # Game over
        if not computer_turn:
            shot_coordinates = handle_mouse_event(event)
            if shot_coordinates is not None:
                flag = False
                for hit_block in const.hit_blocks:
                    if hit_block == shot_coordinates:
                        flag = True
                for dot in const.dotted:
                    if dot == shot_coordinates:
                        flag = True
                if not flag:
                    computer_turn = not logic.hit_or_miss(
                        shot_coordinates, const.COMPUTER_SHIPS, computer_turn)
    if not game_over and computer_turn:
        if const.around_hit_set:
            computer_turn = logic.shot(const.around_hit_set)
        else:
            computer_turn = logic.shot(const.available_to_fire_set)
    return game_over, computer_turn, flag


def init_pygame() -> None:
    """Проделаем стартовые операции pygame"""
    const.HUMAN = ShipDrawer()
    const.HUMAN_SHIPS = copy.deepcopy(const.HUMAN.ships)
    const.COMPUTER = ShipDrawer()
    const.COMPUTER_SHIPS = copy.deepcopy(const.COMPUTER.ships)
    const.screen.fill(const.BLUE)


def play() -> None:
    """Запускает игровой цикл"""
    init_pygame()
    Grid("COMPUTER", 0)
    Grid("HUMAN", const.DISTANCE)
    Drawer.draw_ship(const.HUMAN.ships)
    computer_turn = False
    flag, game_over = display_the_start_screen(False)
    while not game_over:
        game_over, computer_turn, flag = gameplay(game_over, computer_turn, flag)
        Drawer.draw_dots(const.dotted)
        Drawer.hit_blocks(const.hit_blocks)
        Drawer.draw_ship(const.destroyed_ships)
        if not const.COMPUTER.ships_set:
            show_message(
                "YOU WIN!", (0, 0, const.SIZE[0], const.SIZE[1]), const.GAME_OVER)
        if not const.HUMAN.ships_set:
            show_message(
                "YOU LOSE!", (0, 0, const.SIZE[0], const.SIZE[1]), const.GAME_OVER)
            Drawer.draw_ship(const.COMPUTER.ships)
        pygame.display.update()
    pygame.quit()


def show_message(message: str, rectangle: tuple, font=const.font) -> None:
    """
    Выводит сообщение на экран в центре заданного прямоугольника.
    """
    message_width, message_height = font.size(message)
    message_rectangle = pygame.Rect(rectangle)
    x_coordinate = message_rectangle.centerx - message_width / 2
    y_coordinate = message_rectangle.centery - message_height / 2
    background_rect = pygame.Rect(x_coordinate - const.BLOCK_SIZE / 2,
                                  y_coordinate, message_width + const.BLOCK_SIZE, message_height)
    message_rendered = font.render(message, True, const.RED)
    const.screen.fill(const.BLUE, background_rect)
    const.screen.blit(message_rendered, (x_coordinate, y_coordinate))
