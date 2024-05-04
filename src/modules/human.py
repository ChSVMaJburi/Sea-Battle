"""Модуль с реализацией HumanPlayer"""
import pygame
from ..console.message_functions import get_coordinates_from_console
from ..modules.player_class import Player
from ..modules.ship_manager import Point
from .. import global_variables as my_space


class HumanPlayer(Player):
    """Реализуем класс HumanPlayer"""

    def shoot_gui_version(self, other_player: Player) -> bool:
        """Обрабатывает события мыши для игрового поля и определяет, чей сейчас ход.
               В зависимости от событий, она обновляет состояние игры"""
        other_turn = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            shot_coordinates = handle_mouse_event(event)
            if shot_coordinates is not None:
                shoot_taken = False
                for hit_block in self.hit_blocks:
                    if hit_block == shot_coordinates:
                        shoot_taken = True
                for dot in self.dotted:
                    if dot == shot_coordinates:
                        shoot_taken = True
                if not shoot_taken:
                    other_turn = not self.check_is_successful_hit(shot_coordinates, other_player)
        return other_turn

    def shoot(self, other_player: Player) -> bool:
        """Выполняет выстрел от имени игрока"""
        if my_space.IS_PYGAME_INIT:
            return self.shoot_gui_version(other_player)
        destroyed = len(self.destroyed_ships)
        answer = self.check_is_successful_hit(get_coordinates_from_console(self), other_player)
        if len(self.destroyed_ships) > destroyed:
            print("Убил!")
        elif answer:
            print("Попал")
        else:
            print("Промах")
        return answer


def handle_mouse_event(event: pygame.event) -> Point or None:
    """Обрабатывает события мыши для хода игрока."""
    if event.type == pygame.MOUSEBUTTONDOWN:
        x_coordinate, y_coordinate = event.pos
        if (my_space.MIN_X <= x_coordinate <= my_space.MAX_X and
                my_space.MIN_Y <= y_coordinate <= my_space.MAX_Y):
            if ((my_space.LEFT_MARGIN < x_coordinate < my_space.LEFT_MARGIN +
                 my_space.GRID_SIZE * my_space.BLOCK_SIZE) and
                    (my_space.UP_MARGIN < y_coordinate < my_space.UP_MARGIN +
                     my_space.GRID_SIZE * my_space.BLOCK_SIZE)):
                return Point((x_coordinate - my_space.LEFT_MARGIN) // my_space.BLOCK_SIZE + 1,
                             (y_coordinate - my_space.UP_MARGIN) // my_space.BLOCK_SIZE + 1)
    return None
