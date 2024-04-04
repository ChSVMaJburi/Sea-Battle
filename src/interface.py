import copy
import pygame
from button import Button
import global_variables as my_space
from grid_class import Grid
from drawer import Drawer, ShipDrawer

import shooting_process as shooting

pygame.init()

start_game_x_position = my_space.LEFT_MARGIN + my_space.GRID_SIZE * my_space.BLOCK_SIZE
start_button = Button(start_game_x_position, "START GAME")


def display_the_start_screen(game_over: bool) -> tuple[bool, bool]:
    """"Создает кнопку "START GAME", рисует ее на экране и обрабатывает события мыши"""
    shot_taken = True
    while shot_taken:
        start_button.draw_button()
        start_button.change_color_on_hover()
        pygame.display.update()
        mouse_position = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                shot_taken = False
                game_over = True
            elif (event.type == pygame.MOUSEBUTTONDOWN and
                  start_button.rect.collidepoint(mouse_position)):
                shot_taken = False
        pygame.display.update()
        my_space.screen.fill(my_space.BLUE,
                             (my_space.RECTANGLE_X, my_space.RECTANGLE_Y, my_space.RECTANGLE_WIDTH,
                              my_space.RECTANGLE_HEIGHT))
    return shot_taken, game_over


def handle_mouse_event(event):
    """Обрабатывает события мыши для хода игрока."""
    if event.type == pygame.MOUSEBUTTONDOWN:
        x_coordinate, y_coordinate = event.pos
        if (my_space.MIN_X <= x_coordinate <= my_space.MAX_X and
                my_space.MIN_Y <= y_coordinate <= my_space.MAX_Y):
            if ((my_space.LEFT_MARGIN < x_coordinate < my_space.LEFT_MARGIN +
                 my_space.GRID_OFFSET * my_space.BLOCK_SIZE) and
                    (my_space.UP_MARGIN < y_coordinate < my_space.UP_MARGIN +
                     my_space.GRID_OFFSET * my_space.BLOCK_SIZE)):
                return ((x_coordinate - my_space.LEFT_MARGIN) // my_space.BLOCK_SIZE + 1,
                        (y_coordinate - my_space.UP_MARGIN) // my_space.BLOCK_SIZE + 1)
    return None


def shoot(game_over: bool, computer_turn: bool, shot_taken: bool) -> tuple[bool, bool, bool]:
    """Обрабатывает события мыши для игрового поля и определяет, чей сейчас ход.
       В зависимости от событий, она обновляет состояние игры"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True, computer_turn, shot_taken
        if not computer_turn:
            shot_coordinates = handle_mouse_event(event)
            if shot_coordinates is not None:
                shot_taken = False
                for hit_block in my_space.hit_blocks:
                    if hit_block == shot_coordinates:
                        shot_taken = True
                for dot in my_space.dotted:
                    if dot == shot_coordinates:
                        shot_taken = True
                if not shot_taken:
                    computer_turn = not shooting.check_is_successful_hit(
                        shot_coordinates, my_space.COMPUTER_SHIPS, computer_turn)
    if not game_over and computer_turn:
        if my_space.around_hit_set:
            computer_turn = shooting.random_shot(my_space.around_hit_set)
        else:
            computer_turn = shooting.random_shot(my_space.available_to_fire_set)
    return game_over, computer_turn, shot_taken

def play() -> None:
    """Запускает игровой цикл"""
    my_space.HUMAN = ShipDrawer()
    my_space.HUMAN_SHIPS = copy.deepcopy(my_space.HUMAN.ships)
    my_space.COMPUTER = ShipDrawer()
    my_space.COMPUTER_SHIPS = copy.deepcopy(my_space.COMPUTER.ships)
    Grid("COMPUTER", 0)
    Grid("HUMAN", my_space.DISTANCE)
    Drawer.draw_ship(my_space.HUMAN.ships)
    computer_turn = False
    shot_taken, game_over = display_the_start_screen(False)
    while not game_over:
        game_over, computer_turn, shot_taken = shoot(game_over, computer_turn, shot_taken)
        Drawer.draw_dots(my_space.dotted)
        Drawer.draw_hit_blocks(my_space.hit_blocks)
        Drawer.draw_ship(my_space.destroyed_ships)
        if not my_space.COMPUTER.ships_set:
            show_message(
                "YOU WIN!", (0, 0, my_space.SIZE[0], my_space.SIZE[1]), my_space.GAME_OVER)
        if not my_space.HUMAN.ships_set:
            show_message(
                "YOU LOSE!", (0, 0, my_space.SIZE[0], my_space.SIZE[1]), my_space.GAME_OVER)
            Drawer.draw_ship(my_space.COMPUTER.ships)
        pygame.display.update()
    pygame.quit()


def show_message(message: str, rectangle: tuple, font=my_space.font) -> None:
    """
    Выводит сообщение на экран в центре заданного прямоугольника.
    """
    message_width, message_height = font.size(message)
    message_rectangle = pygame.Rect(rectangle)
    x_coordinate = message_rectangle.centerx - message_width / 2
    y_coordinate = message_rectangle.centery - message_height / 2
    background_rect = pygame.Rect(x_coordinate - my_space.BLOCK_SIZE / 2,
                                  y_coordinate, message_width + my_space.BLOCK_SIZE, message_height)
    message_rendered = font.render(message, True, my_space.RED)
    my_space.screen.fill(my_space.BLUE, background_rect)
    my_space.screen.blit(message_rendered, (x_coordinate, y_coordinate))
