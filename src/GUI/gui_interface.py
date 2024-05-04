"""Основной цикл игры и вспомогательные функции"""
import pygame
from src.GUI.button import Button
import src.global_variables as my_space
from src.GUI.gui_drawer import Drawer
from src.GUI.grid_class import Grid
from src.modules.human import HumanPlayer
from src.modules.computer import ComputerPlayer


def main_menu():
    """"Создает кнопки, рисует их на экране и обрабатывает события мыши"""
    start_game_position = my_space.LEFT_MARGIN + (my_space.GRID_SIZE - 2.2) * my_space.BLOCK_SIZE
    start_button = Button(start_game_position, 0, "START GAME WITH COMPUTER")
    exit_game_position = my_space.LEFT_MARGIN + my_space.GRID_SIZE * my_space.BLOCK_SIZE
    exit_button = Button(exit_game_position, 100, "EXIT GAME")
    show_message("Welcome to the Battleship game",
                 my_space.WELCOME_RECTANGLE)
    shot_taken = True
    while shot_taken:
        start_button.draw_button()
        start_button.change_color_on_hover()
        exit_button.draw_button()
        exit_button.change_color_on_hover()
        pygame.display.update()
        mouse_position = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                    event.type == pygame.MOUSEBUTTONDOWN and exit_button.rect.collidepoint(mouse_position)):
                exit(0)
            elif (event.type == pygame.MOUSEBUTTONDOWN and
                  start_button.rect.collidepoint(mouse_position)):
                shot_taken = False
        pygame.display.update()
    my_space.screen.fill(my_space.SCREEN_COLOR, my_space.WELCOME_RECTANGLE)


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
    main_menu()
    grids = (Grid("YOU", 0), Grid("YOU", my_space.DISTANCE))
    grids[0].start_drawing()
    grids[1].start_drawing()

    human = HumanPlayer(0)
    computer = ComputerPlayer(my_space.DISTANCE)
    Drawer.draw_rectangles(human.ship_manager.ships, computer.offset)
    # Drawer.draw_rectangles(computer.ship_manager.ships, human.offset)
    turn_two, game_over = False, False
    while not game_over:
        if turn_two:
            turn_two = computer.shoot(human)
        else:
            turn_two = human.shoot(computer)

        Drawer.draw_dots(human.dotted | computer.dotted)
        Drawer.draw_hit_blocks(human.hit_blocks | computer.hit_blocks)
        Drawer.draw_rectangles(human.destroyed_ships, human.offset)
        if not computer.ship_manager.ships_set:
            show_message(
                "YOU WIN!", my_space.END_RECTANGLE)
            game_over = True
        if not human.ship_manager.ships_set:
            show_message(
                "YOU LOSE!", my_space.END_RECTANGLE)
            game_over = True
            Drawer.draw_rectangles(computer.ship_manager.ships, human.offset)
        pygame.display.update()
    check_restart()


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
