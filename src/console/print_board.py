"""Файл для вывода доски"""
import src.global_variables as my_space
from src.console.support_functions import ask_question
from src.modules.players import Player
from src.modules.ship_manager import Point


def print_board(first: Player, second: Player) -> None:
    """"Процедура выбирающая как именно вывести доски"""
    if my_space.ASKED_FLAG == 2:
        show_horizontal(first, second)
    elif my_space.ASKED_FLAG == 1:
        show_vertically(first, second)
    else:
        my_space.ASKED_FLAG = 1 + ask_question(
            "Желаете, чтобы игровые поля показывались горизонтально?")
        print_board(first, second)


def print_corner(enter: str) -> None:
    """Функция помогающая облегчить вывод. Выводит клетки"""
    for j in range(21):
        if j % 2 == 0:
            if j != 20:
                print("├─", end="")
            else:
                print("┤", end=enter)
        else:
            print("──", end="")


def GetSymbol(player: Player, coordinate: Point, showing_ship: bool) -> chr:
    """Выдаёт нужный символ для вывода"""
    if coordinate in player.injured:
        return 'X'
    if coordinate in player.missed:
        return '*'
    if showing_ship:
        for ship in player.ship_manager.ships_copy:
            if coordinate in ship:
                return '□'
    return ' '


def print_num_in_corner(player: Player, row: int, enter: str, showing_ship: bool) -> None:
    """Функция помогающая облегчить вывод. Выводит значение в клетке"""
    for column in range(21):
        if column % 2 == 0:
            if column != 20:
                print("│", end="")
            else:
                print("│", end=enter)
        else:
            print(f" {GetSymbol(player, Point(row // 2 + 1, column // 2 + 1), showing_ship)} ", end="")


def make_distance() -> None:
    """Создаёт дистанцию для вывода игровых полей"""
    print(" " * my_space.DISTANCE, end="")


def print_letters() -> None:
    """Выводит буквы для доски"""
    for column in range(my_space.GRID_SIZE * 2):
        if column % 2 == 0:
            print(f"  {my_space.LETTERS[column // 2]} ", end="")
    print("    ", end='')


def print_num(number: int) -> None:
    """Выводит числа для доски"""
    if number < 10:
        print(" ", end="")
    print(number, end=" ")


def show_horizontal(first: Player, second: Player) -> None:
    """Выводит доски горизонтально"""
    first_size = len(first.name)
    print("    ", end="")
    print(first.name, second.name,
          sep=" " * (my_space.REAL_DISTANCE - first_size), end="\n   ")
    print_letters()
    make_distance()
    print_letters()
    print()
    for row in range(my_space.GRID_SIZE * 2 + 1):
        if row % 2 == 0:
            print("   ", end="")
            print_corner("")
            make_distance()
            print("   ", end="")
            print_corner("\n")
        else:
            print_num((row + 1) // 2)
            print_num_in_corner(first, row, "", True)
            make_distance()
            print_num((row + 1) // 2)
            print_num_in_corner(second, row, "\n", False)


def show_board(player: Player, showing_ship: bool) -> None:
    """Выводит одну доску"""
    print(" " * my_space.DISTANCE, player.name, end="\n   ")
    print_letters()
    print()
    for row in range(my_space.GRID_SIZE * 2 + 1):
        print_num(row + 1)
        if row % 2 == 0:
            print_corner("\n")
        else:
            print_num_in_corner(player, row, "\n", showing_ship)


def show_vertically(first: Player, second: Player) -> None:
    """Выводит доски вертикально"""
    show_board(first, True)
    print()
    show_board(second, False)
