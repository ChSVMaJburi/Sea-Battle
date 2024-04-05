"""Реализация вспомогательных функций"""


def yes_or_no_lower(text: str) -> str:
    """Почему-то lower() в некоторых случаях плохо работал с кириллицей,
    решил написать свою мини аналогию"""
    answer = ""
    for char in text:
        if char == 'Д':
            char = 'д'
        if char == 'А':
            char = 'а'
        if char == 'Н':
            char = 'н'
        if char == 'Е':
            char = 'е'
        if char == 'Т':
            char = 'т'
        answer += char
    return answer


def ask_question(message: str) -> bool:
    """Функция для общения с пользователем в формате Да/Нет"""
    print(message, "[Д\н]")
    choice = yes_or_no_lower(input())
    if choice == "д" or choice == "да":
        return True
    if choice == "н" or choice == "нет":
        return False
    print("Похоже, что вы неправильно ввели ;( Повторите, пожалуйста")
    return ask_question(message)
