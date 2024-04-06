"""Реализуем классы Player, HumanPlayer"""
from abc import ABC, abstractmethod
from typing import Tuple
from src.GUI.gui_drawer import Point
from src.modules.ship_manager import ShipManager


class Player(ABC):
    """Реализуем класс Player"""

    def __init__(self, name: str, offset: int):
        self.name = name
        self.offset = offset
        self.ship_manager = ShipManager()
        self.hit_blocks = set[Point]()
        self.dotted = set[Point]()
        self.injured = set[Point]()
        self.missed = set[Point]()

    @abstractmethod
    def update_dotted_and_hit(self, shot_coordinates: Point,
                              diagonal_only: bool) -> None:
        """Эта процедура добавляет точки вокруг клетки, в которую был произведен выстрел"""

    @abstractmethod
    def shoot(self, other_player, shot_taken: bool) -> Tuple[bool, bool]:
        """Обрабатывает события мыши для игрового поля и определяет, чей сейчас ход.
               В зависимости от событий, она обновляет состояние игры"""

    def process_destroyed_ship(self, pos: int, other_player, diagonal_only: bool) -> None:
        """
        Обрабатывает процесс уничтожения корабля
        """
        ship = sorted(other_player.ship_manager.ships[pos])
        for ind in range(-1, 1):
            self.update_dotted_and_hit(ship[ind], diagonal_only)
        # Drawer().draw_ship(other_player.drawer.ships[pos], 0)
