"""Реализация функций для вывода и ввода с консоли"""
from src.modules.player_class import Player
from src.modules.ship_manager import Point


def print_error() -> None:
    """Функция для вывода ошибки"""
    print("Похоже, что вы неправильно ввели ;( Повторите, пожалуйста.")


def ask_question(message: str) -> bool:
    """Функция для общения с пользователем в формате Yes/No"""
    choice = send_message(message + " [Y\\n]").lower()
    if choice == "y" or choice == "yes":
        return True
    if choice == "n" or choice == "no":
        return False
    print_error()
    return ask_question(message)


def send_message(message: str) -> str:
    """Функция, для вывода в консоль строки message и получения ответа"""
    print(message)
    return input()


def check_valid_number(number: str) -> bool:
    """Проверка на валидную строку"""
    try:
        number = int(number)
    except ValueError:
        return False
    return 1 <= number <= 10


def check_valid_letter(letter: str) -> bool:
    """Проверка на валидную строку"""
    return len(letter) == 1 and letter.isalpha() and letter.isupper() and 'A' <= letter <= 'J'


def get_coordinates_from_console(player: Player) -> Point:
    """Функция для получения координат с консоли"""
    coordinate = send_message(
        "Ваш ход.\nВведите пожалуйста координаты в формате: \"A1\"(буква и число)")
    if (len(coordinate) != 2 or not check_valid_number(coordinate[1]) or
            not check_valid_letter(coordinate[0])):
        if not (len(coordinate) == 3 and check_valid_number(coordinate[1:3])
                and check_valid_letter(coordinate[0])):
            print_error()
            return get_coordinates_from_console(player)
    answer = Point(int(coordinate[1] + (coordinate[2] if len(coordinate) == 3 else "")),
                   ord(coordinate[0]) - ord('A') + 1)
    if answer in player.hit_blocks:
        print("Вы уже стреляли в эту координату.")
        print_error()
        return get_coordinates_from_console(player)
    if answer in player.dotted:
        print("Вы точно знаете, что по этой координате нет корабля.")
        print_error()
        return get_coordinates_from_console(player)
    return answer
