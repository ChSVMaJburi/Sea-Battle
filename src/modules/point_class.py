"""Реализация класса Point"""
from typing import Iterator, Tuple


class Point:
    """Класс схожий с Tuple[int, int] для упрощения кода"""

    def __init__(self, x_coordinate: int, y_coordinate: int) -> None:
        self.coordinate = (x_coordinate, y_coordinate)

    def __lt__(self, other: 'Point') -> bool:
        return self.coordinate < other.coordinate

    def __getitem__(self, index: int) -> int:
        return self.coordinate[index]

    def __iter__(self) -> Iterator[Tuple[int, int]]:
        return iter(self.coordinate)

    def __repr__(self) -> str:
        return f"({self.coordinate[0]}, {self.coordinate[1]})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Point):
            return False
        return self.coordinate == other.coordinate

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return hash((self.coordinate, self.coordinate))

    def __is__(self, other: 'Point') -> bool:
        return self == other
