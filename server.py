import asyncio
import pickle
import sys


class GameServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.players = []

    async def handle_client(self, reader, writer):
        player_id = len(self.players) + 1
        self.players.append(writer)
        print(f"Player {player_id} connected.")
        started = False
        try:
            while True:
                # print(f"Player {player_id} cnt -> {len(self.players)} writer -> {writer}")
                if not started and len(self.players) == 2:
                    writer.write(pickle.dumps(False if writer is self.players[0] else True))
                    await writer.drain()
                    started = True

                try:
                    data = await asyncio.wait_for(reader.read(1024), timeout=0.1)
                    print(pickle.loads(data))
                except asyncio.TimeoutError:
                    continue
                if not data:
                    print(f"Player {player_id} disconnected maybe?")
                    self.players.remove(writer)
                    sys.exit(1)
                print(f"Received from Player {player_id}")
                other_player_writer = self.players[1] if writer is self.players[0] else self.players[0]
                other_player_writer.write(data)
                await other_player_writer.drain()

        except ConnectionResetError:
            print(f"Player {player_id} disconnected.")
            sys.exit(1)

    async def start(self):
        server = await asyncio.start_server(
            self.handle_client, self.host, self.port)
        async with server:
            await server.serve_forever()


async def main():
    server = GameServer('127.0.0.1', 8888)
    await server.start()


if __name__ == "__main__":
    asyncio.run(main())
