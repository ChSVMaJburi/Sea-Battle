import pickle
import socket
from typing import Tuple

import pygame

from . import global_variables as my_space
from src.GUI.text_manager import TextManager


class BattleshipClient:
    """Класс для клиента"""

    def __init__(self, server_host, server_port):
        self.server_host = server_host
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.client_socket.connect((self.server_host, self.server_port))
        print("Подключение к серверу {}:{}".format(self.server_host, self.server_port))

    def send_data_to_server(self, data):
        self.client_socket.sendall(pickle.dumps(data))

    def receive_data_from_server(self):
        return pickle.loads(self.client_socket.recv(4096))

    def close(self):
        self.client_socket.close()


def get_host_and_port() -> Tuple[str, int]:
    """Функция для ввода хоста"""
    TextManager("In 'IP::PORT' format please. Example: 192.168.1.1:8001").print_to_gui(my_space.IP_COORD)
    host_text = TextManager("")
    TextManager("IP::PORT: ").print_to_gui(my_space.BEFORE_INPUT)
    while True:
        my_space.screen.fill(my_space.SCREEN_COLOR, my_space.INPUT_RECTANGLE)
        returned = host_text.input_from_gui()
        if returned and correct_host(host_text.text):
            host, port = host_text.text.split(':')
            return host, int(port)
        elif returned:
            for i in range(1000):
                TextManager("Failed").print_to_gui(my_space.INPUT_COORDINATE)
                pygame.display.update()
            host_text.text = ""
        else:
            host_text.print_to_gui(my_space.INPUT_COORDINATE)
        pygame.display.update()


def correct_host(text: str) -> bool:
    """Функция для проверки хоста на корректность"""
    if len(text.split(":")) != 2:
        return False
    host, port = text.split(":")
    try:
        port = int(port)
    except ValueError:
        return False
    if host == "localhost":
        return True
    host = host.split('.')
    if len(host) != 4:
        return False
    try:
        host[0], host[1], host[2], host[3] = int(host[0]), int(host[1]), int(host[2]), int(host[3])
    except ValueError:
        return False
    return True
