"""Реализуется консольная версия интерфейса"""
import src.global_variables as my_space
from src.modules.human import HumanPlayer
from src.modules.computer import ComputerPlayer
from src.console.print_board import print_board
from src.console.message_functions import say_goodbye


# from src.console.console_drawer import ConsoleBoard


def play_console_type():
    """Запускает игровой цикл"""
    print("Приветствую в консольной версии :)")
    human = HumanPlayer("HUMAN", 0)
    computer = ComputerPlayer("COMPUTER", my_space.DISTANCE)
    turn_two = False
    print_board(human, computer)
    while True:
        if not turn_two:
            is_success, _ = human.shoot(computer, True)
        else:
            is_success, _ = computer.shoot(human, True)
        if ((turn_two and not is_success) or (not turn_two and is_success) or
                not human.ship_manager.ships_set or not computer.ship_manager.ships_set):
            print_board(human, computer)
        if not is_success:
            turn_two ^= 1
        if not human.ship_manager.ships_set:
            say_goodbye(computer)
            return
        if not computer.ship_manager.ships_set:
            say_goodbye(human)
            return
