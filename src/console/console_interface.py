"""Реализуется консольная версия интерфейса"""
import src.global_variables as my_space
from src.modules.players import HumanPlayer
from src.modules.computer import ComputerPlayer
from src.console.print_board import print_board


# from src.console.console_drawer import ConsoleBoard


def play_console_type():
    """Запускает игровой цикл"""
    print("Приветствую в консольной версии :)")
    human = HumanPlayer("HUMAN", 0)
    computer = ComputerPlayer("COMPUTER", my_space.DISTANCE)
    game_over = False
    while not game_over:
        print_board(human, computer)

