"""Реализация вспомогательных функций"""

def ask_question(message: str) -> bool:
    """Функция для общения с пользователем в формате Yes/No"""
    print(message, "[Y\\n]")
    choice = input().lower()
    if choice == "y" or choice == "yes":
        return True
    if choice == "n" or choice == "no":
        return False
    print("Похоже, что вы неправильно ввели ;( Повторите, пожалуйста")
    return ask_question(message)
