"""Основной файл"""
from src.GUI.gui_interface import play_gui_type
from src.console.console_interface import play_console_type
import sys

from src.console.message_functions import ask_question

sys.stdin = open(sys.stdin.fileno(), mode='r', encoding='utf-8', buffering=True)

if __name__ == "__main__":
    print("\nПривет!\n")
    if ask_question("Желаете воспользоваться графическим интерфейсом?"):
        play_gui_type()
    else:
        play_console_type()
    # play_console_type()
    # play_gui_type()
