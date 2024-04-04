import pygame
from button import Button
import global_variables as my_space
from drawer import Drawer
from players import HumanPlayer
from computer import ComputerPlayer

pygame.init()

START_GAME_X_POSITION = my_space.LEFT_MARGIN + my_space.GRID_SIZE * my_space.BLOCK_SIZE
start_button = Button(START_GAME_X_POSITION, "START GAME")


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


def play() -> None:
    """Запускает игровой цикл"""
    human = HumanPlayer("HUMAN", 0)
    computer = ComputerPlayer("COMPUTER", my_space.MAX_X_OFFSET)
    Drawer.draw_ship(human.drawer.ships, computer.offset)
    Drawer.draw_ship(computer.drawer.ships, human.offset)
    turn_two = False
    shot_taken, game_over = display_the_start_screen(False)
    while not game_over:
        if turn_two:
            game_over, turn_two, shot_taken = computer.shoot(human, game_over, shot_taken)
        else:
            game_over, turn_two, shot_taken = human.shoot(computer, game_over, shot_taken)

        Drawer.draw_dots(human.dotted | computer.dotted)
        Drawer.draw_hit_blocks(human.hit_blocks | computer.hit_blocks)
        # Drawer.draw_ship(human.destroyed_ships, human.offset)
        if not computer.drawer.ships_set:
            show_message(
                "YOU WIN!", (0, 0, my_space.SIZE[0], my_space.SIZE[1]), my_space.GAME_OVER)
        if not human.drawer.ships_set:
            show_message(
                "YOU LOSE!", (0, 0, my_space.SIZE[0], my_space.SIZE[1]), my_space.GAME_OVER)
            Drawer.draw_ship(computer.drawer.ships, human.offset)
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
