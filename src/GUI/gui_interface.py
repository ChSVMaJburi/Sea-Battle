"""Основной цикл игры и вспомогательные функции"""
from typing import Tuple

import pygame
from src.GUI.button import Button
import src.global_variables as my_space
from src.GUI.gui_drawer import Drawer
from src.GUI.grid_class import Grid
from src.GUI.text_manager import TextManager
from src.modules.human import HumanPlayer
from src.modules.computer import ComputerPlayer, update_around_comp_hit
from src.modules.player_class import Player


def update_all_buttons(buttons: list[Button]):
    for button in buttons:
        button.draw_button()
        button.change_color_on_hover()


def main_menu() -> bool:
    """"Создает кнопки, рисует их на экране и обрабатывает события мыши"""
    with_human_button = Button(my_space.WITH_HUMAN, 0, "START GAME WITH OTHER HUMAN")
    with_computer_button = Button(my_space.WITH_COMPUTER, 100, "START GAME WITH COMPUTER")
    exit_button = Button(my_space.EXIT_GAME, 200, "EXIT GAME")
    show_message("Welcome to the Battleship game",
                 my_space.WELCOME_RECTANGLE)
    shoot_taken = True
    with_human = False
    while shoot_taken:
        update_all_buttons([with_human_button, with_computer_button, exit_button])
        pygame.display.update()
        mouse_position = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                    event.type == pygame.MOUSEBUTTONDOWN and exit_button.rect.collidepoint(mouse_position)):
                exit(0)
            elif (event.type == pygame.MOUSEBUTTONDOWN and
                  with_computer_button.rect.collidepoint(mouse_position)):
                shoot_taken = False
            elif (event.type == pygame.MOUSEBUTTONDOWN and
                  with_human_button.rect.collidepoint(mouse_position)):
                with_human = True
                shoot_taken = False
        pygame.display.update()
    my_space.screen.fill(my_space.SCREEN_COLOR, my_space.WELCOME_RECTANGLE)
    return with_human


def check_restart():
    restart_game_position = my_space.LEFT_MARGIN + (my_space.GRID_SIZE - 0.5) * my_space.BLOCK_SIZE
    restart_button = Button(restart_game_position, 0, "RESTART GAME")
    shot_taken = True
    while shot_taken:
        restart_button.draw_button()
        restart_button.change_color_on_hover()
        pygame.display.update()
        mouse_position = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
            elif (event.type == pygame.MOUSEBUTTONDOWN and
                  restart_button.rect.collidepoint(mouse_position)):
                shot_taken = False
        pygame.display.update()
    my_space.screen.fill(my_space.SCREEN_COLOR, my_space.WELCOME_RECTANGLE)
    play_gui_type()


def play_gui_type() -> None:
    """Запускает игровой цикл"""
    pygame.init()
    with_human = main_menu()
    if not with_human:
        play_with_computer()
        check_restart()
    else:
        host, port = get_host_and_port()


def get_host_and_port() -> Tuple[str, str]:
    """Функция для ввода хоста"""
    entered = False
    show_message("Enter the IP and Port.", my_space.WELCOME_RECTANGLE)
    show_message("In IP::PORT format please.", my_space.IP_RECTANGLE)
    host_text = TextManager("")
    TextManager("IP::PORT: ").print_to_gui(my_space.BEFORE_INPUT)
    while not entered:
        my_space.screen.fill(my_space.SCREEN_COLOR, my_space.INPUT_RECTANGLE)
        returned = host_text.input_from_gui()
        if returned and correct_host(host_text.text):
            pass
        elif returned:
            TextManager("Failed").print_to_gui(my_space.INPUT_COORDINATE)
            host_text.text = ""
        else:
            host_text.print_to_gui(my_space.INPUT_COORDINATE)
        pygame.display.update()


def correct_host(text: str) -> bool:
    """Функция для проверки хоста на корректность"""
    if len(text.split(":")) != 2:
        return False


def play_with_computer():
    """Функция для игры против компьютера"""
    grids = (Grid("YOU", 0), Grid("OTHER PLAYER", my_space.DISTANCE))
    grids[0].start_drawing()
    grids[1].start_drawing()
    you = HumanPlayer(0)
    other_player = ComputerPlayer(my_space.DISTANCE)
    Drawer.draw_rectangles(you.ship_manager.ships, other_player.offset)
    # Drawer.draw_rectangles(other_player.ship_manager.ships, you.offset)
    another_turn, game_over = False, False
    while not game_over:
        if another_turn:
            to_shooting = other_player.shoot()
            another_turn, is_destroyed = you.check_is_successful_hit(to_shooting)
            other_player.process_after_shoot(to_shooting, another_turn, is_destroyed)
            if another_turn:
                other_player.need_to_fire.clear()
            update_around_comp_hit(to_shooting, another_turn, other_player)
        else:
            to_shooting = you.shoot()
            if to_shooting:
                another_turn, is_destroyed = other_player.check_is_successful_hit(to_shooting)
                you.process_after_shoot(to_shooting, another_turn, is_destroyed)
                another_turn = not another_turn

        Drawer.draw_dots(you.dotted | other_player.dotted)
        Drawer.draw_hit_blocks(you.hit_blocks | other_player.hit_blocks)
        Drawer.draw_rectangles(you.destroyed_ships, you.offset)
        check_end_game(you, other_player)
        pygame.display.update()


def check_end_game(first: Player, second: Player):
    if not second.ship_manager.ships_set:
        show_message(
            "YOU WIN!", my_space.END_RECTANGLE)
        game_over = True
    if not first.ship_manager.ships_set:
        show_message(
            "YOU LOSE!", my_space.END_RECTANGLE)
        game_over = True
        Drawer.draw_rectangles(second.ship_manager.ships, first.offset)


def show_message(message: str, rectangle: tuple, color=my_space.MESSAGE_COLOR) -> None:
    """
    Выводит сообщение на экран в центре заданного прямоугольника.
    """
    message_width, message_height = my_space.GAME_OVER.size(message)
    message_rectangle = pygame.Rect(rectangle)
    x_coordinate = message_rectangle.centerx - message_width / 2
    y_coordinate = message_rectangle.centery - message_height / 2
    background_rect = pygame.Rect(x_coordinate - my_space.BLOCK_SIZE / 2,
                                  y_coordinate, message_width + my_space.BLOCK_SIZE, message_height)
    message_rendered = my_space.GAME_OVER.render(message, True, color)
    my_space.screen.fill(my_space.SCREEN_COLOR, background_rect)
    my_space.screen.blit(message_rendered, (x_coordinate, y_coordinate))
