"""Реализуется консольная версия интерфейса"""
import src.global_variables as my_space
from src.modules.human import HumanPlayer
from src.modules.computer import ComputerPlayer
from src.console.print_board import print_board


def play_console_type():
    """Запускает игровой цикл"""
    print("Приветствую в консольной версии :)")
    you = HumanPlayer(0)
    other_player = ComputerPlayer(my_space.DISTANCE)
    turn_two = False
    print_board(you, other_player)
    while True:
        if not turn_two:
            is_success = you.shoot(other_player)
        else:
            is_success = other_player.shoot(you)
        if ((turn_two and not is_success) or (not turn_two and is_success) or
                not you.ship_manager.ships_set or not other_player.ship_manager.ships_set):
            print_board(you, other_player)
        if not is_success:
            turn_two ^= 1
        if not you.ship_manager.ships_set:
            print("Вы проиграли")
            return
        if not other_player.ship_manager.ships_set:
            print("Вы выиграли")
            return
