"""Основной цикл игры и вспомогательные функции"""
import copy
from typing import Tuple, Set

import asyncio
import pygame
from src.GUI.button import Button
import src.global_variables as my_space
from src.GUI.gui_drawer import Drawer
from src.GUI.grid_class import Grid
from src.GUI.text_manager import TextManager
from src.client import GameClient
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
        return
    asyncio.run(play_with_human())
    check_restart()


async def play_with_human() -> None:
    show_message("Enter the IP and Port.", my_space.WELCOME_RECTANGLE)
    # host, port = get_host_and_port()
    host, port = "127.0.0.1", 8888
    client = GameClient(host, port)
    my_dotted, my_hit_blocks = set(), set()
    try:
        print("ok")
        await asyncio.create_task(client.connect())
        print("ok")
        my_space.screen.fill(my_space.SCREEN_COLOR, my_space.WELCOME_RECTANGLE)
        grids = (Grid("YOU", 0), Grid("OTHER PLAYER", my_space.DISTANCE))
        grids[0].start_drawing()
        grids[1].start_drawing()
        you = HumanPlayer(0)
        Drawer.draw_rectangles(you.ship_manager.ships, my_space.DISTANCE)
        print("ok")
        another_turn, game_over = await client.receive_data(), False
        while not game_over:
            if another_turn:
                to_shooting = await client.receive_data()
                print(to_shooting, "opponent")
                another_turn, is_destroyed = you.check_is_successful_hit(to_shooting)
                await client.send_data((another_turn, is_destroyed))
            else:
                to_shooting = you.shoot()
                if to_shooting:
                    print(to_shooting, "me")
                    await client.send_data(to_shooting)
                    another_turn, is_destroyed = await client.receive_data()
                    you.process_after_shoot(to_shooting, another_turn, is_destroyed)
                    another_turn = not another_turn
                else:
                    pygame.display.update()
                    continue
            game_over, my_dotted, my_hit_blocks = await update_display(client, you, my_dotted, my_hit_blocks)
    except KeyboardInterrupt:
        print("Отключение от сервера.")
        await client.close()


async def update_display(client: GameClient, you: Player, my_last_dotted: Set, my_last_hit_blocks: Set) \
        -> Tuple[bool, Set, Set]:
    """Действия для обновления экрана"""
    print(you.hit_blocks, " --- ", my_last_hit_blocks,
          len(you.ship_manager.ships_set), "my hits")
    await client.send_data(you.dotted - my_last_dotted)
    other_dotted = await client.receive_data()
    print("dots received", other_dotted)
    await asyncio.sleep(0.2)
    await client.send_data(you.hit_blocks - my_last_hit_blocks)
    other_hit_blocks = await client.receive_data()
    print("hit_blocks received", other_hit_blocks)
    await asyncio.sleep(0.2)
    await client.send_data(len(you.ship_manager.ships_set))
    other_len = await client.receive_data()
    print("len received", other_len)
    my_last_dotted, my_last_hit_blocks = copy.deepcopy(you.dotted), copy.deepcopy(you.hit_blocks)

    for dot in other_dotted:
        dot.coordinate = \
            (dot.coordinate[0] + my_space.DISTANCE, dot.coordinate[1])
    for hit_block in other_hit_blocks:
        hit_block.coordinate = \
            (hit_block.coordinate[0] + my_space.DISTANCE, hit_block.coordinate[1])

    Drawer.draw_dots(you.dotted | other_dotted)
    Drawer.draw_hit_blocks(you.hit_blocks | other_hit_blocks)
    Drawer.draw_rectangles(you.destroyed_ships, you.offset)
    game_over = check_end_game(len(you.ship_manager.ships_set),
                               other_len)
    pygame.display.update()
    return game_over, my_last_dotted, my_last_hit_blocks


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
        game_over = check_end_game(len(you.ship_manager.ships_set),
                                   len(other_player.ship_manager.ships_set))
        pygame.display.update()


def check_end_game(first_count: int, second_count: int) -> bool:
    game_over = False
    if second_count == 0:
        show_message(
            "YOU WIN!", my_space.END_RECTANGLE)
        game_over = True
    if first_count == 0:
        show_message(
            "YOU LOSE!", my_space.END_RECTANGLE)
        game_over = True
    return game_over


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
