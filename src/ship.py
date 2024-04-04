"""Реализация класса Ship"""
from typing import List, Tuple


class Ship:
    def __init__(self, coordinates: List[Tuple[int, int]]):
        self.coordinates = set(coordinates)

    def __len__(self):
        return len(self.coordinates)

    def __contains__(self, item):
        return item in self.coordinates

    def update_coordinates(self, new_coordinates: List[Tuple[int, int]]):
        self.coordinates = set(new_coordinates)

    def add_coordinate(self, coordinate: Tuple[int, int]):
        self.coordinates.add(coordinate)

    def remove_coordinate(self, coordinate: Tuple[int, int]):
        self.coordinates.remove(coordinate)

    def is_destroyed(self):
        return not self.coordinates
