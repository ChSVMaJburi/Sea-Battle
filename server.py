import pickle
import socket
import threading


class BattleshipServer:
    """Класс для сервера"""

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connections = []
        self.game_started = False

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(2)
        print(f"Сервер запущен на {self.host}:{self.port}")

        while True:
            if self.connections and not self.connections[-1].recv(1024):
                print("Отключился игрок:", self.connections[-1])
                self.connections.pop().close()

            client_socket, client_address = self.server_socket.accept()
            print("Подключен игрок:", client_address)
            self.connections.append(client_socket)
            if len(self.connections) == 2:
                self.start_game()

    def start_game(self):
        self.game_started = True
        print("Игра началась!")
        self.connections[1].send(pickle.dumps(True))
        self.connections[0].send(pickle.dumps(False))
        thread1 = threading.Thread(target=self.handle_player, args=(self.connections[0], self.connections[1]))
        thread2 = threading.Thread(target=self.handle_player, args=(self.connections[1], self.connections[0]))

        thread1.start()
        thread2.start()

    def handle_player(self, player_socket, opponent_socket):
        while True:
            try:
                shoot_data = player_socket.recv(4096)
                if not shoot_data:
                    print("Игрок {} отключился.".format(player_socket.getpeername()))
                    break
                print(player_socket, opponent_socket, " peredacha information")
                opponent_socket.sendall(shoot_data)
            except Exception as e:
                print("Ошибка при обработке данных:", e)
                break

    def close(self):
        self.server_socket.close()


if __name__ == "__main__":
    HOST = "localhost"
    PORT = 1233

    server = BattleshipServer(HOST, PORT)
    try:
        server.start()
    except KeyboardInterrupt:
        print("Сервер остановлен.")
        server.close()
