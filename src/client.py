import asyncio
import pickle
import sys

import pygame


class GameClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.reader = None
        self.writer = None

    async def connect(self):
        self.reader, self.writer = await asyncio.open_connection(self.host, self.port)
        print("Connected to the server.")

    async def send_data(self, data):
        serialized_data = self.serialize_data(data)
        self.writer.write(serialized_data)
        await self.writer.drain()

    async def updating(self, task):
        while not task.done():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
            pygame.display.update()
            await asyncio.sleep(0)

    async def receive_data(self):
        task1 = asyncio.create_task(self.reader.read(1024))
        task2 = asyncio.create_task(self.updating(task1))
        await asyncio.gather(task1, task2)
        return self.deserialize_data(task1.result())

    def serialize_data(self, data):
        serialized_data = pickle.dumps(data)
        return serialized_data

    def deserialize_data(self, data):
        deserialized_data = pickle.loads(data)
        return deserialized_data

    async def close(self):
        self.writer.close()
        await self.writer.wait_closed()
        print("Connection closed.")
