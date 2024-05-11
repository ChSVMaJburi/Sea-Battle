"""Основной файл"""
from src.GUI.gui_interface import play_gui_type
from src.console.console_interface import play_console_type

from src.console.message_functions import ask_question

if __name__ == "__main__":
    print("\nПривет!\n")
    if ask_question("Желаете воспользоваться графическим интерфейсом?"):
        play_gui_type()
    else:
        while True:
            play_console_type()
    # play_console_type()
    # play_gui_type()
