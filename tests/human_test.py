import unittest

from src.modules.human import HumanPlayer
from src.modules.player_class import Player
from src.modules.point_class import Point


class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.player = HumanPlayer(0)

    def test_update_dotted_and_hit(self):
        shot_coordinates = Point(1, 1)
        self.player.update_dotted_and_hit(shot_coordinates, diagonal_only=False)
        self.assertIn(shot_coordinates, self.player.hit_blocks)
        self.assertFalse(all(point in self.player.dotted for point in self.player.dotted_to_shot))

    def test_process_after_shoot(self):
        shot = Point(2, 3)
        self.player.process_after_shoot(shot, is_hit=True, is_destroyed=False)
        self.assertIn(shot, self.player.last_hits)

    def test_check_is_successful_hit(self):
        shot = Point(4, 5)
        self.player.ship_manager.ships_copy = [[Point(4, 5), Point(4, 6)], [Point(6, 7)]]
        is_hit, is_destroyed = self.player.check_is_successful_hit(shot)
        self.assertTrue(is_hit)
        self.assertFalse(is_destroyed)
        is_hit, is_destroyed = self.player.check_is_successful_hit(Point(6, 7))
        self.assertTrue(is_hit)
        self.assertTrue(is_destroyed)
