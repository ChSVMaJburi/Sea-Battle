import unittest

from src.modules.human import HumanPlayer
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

    def test_add_missed_after_miss_1(self):
        self.player.ship_manager.ships_copy = [[Point(4, 5), Point(4, 6)], [Point(6, 7)]]
        shot = Point(6, 8)
        self.player.check_is_successful_hit(shot)
        self.assertIn(shot, self.player.missed)

    def test_add_destroyed_ship_after_hit(self):
        shot = Point(2, 3)
        self.player.ship_manager.ships_copy = [[Point(2, 3)], [Point(4, 5)]]
        self.player.check_is_successful_hit(shot)
        assert not self.player.destroyed_ships

    def test_clear_last_hits_after_destroyed_ship(self):
        shot = Point(3, 4)
        self.player.ship_manager.ships_copy = [[Point(3, 4)]]
        self.player.check_is_successful_hit(shot)
        self.assertFalse(self.player.last_hits)

    def test_remove_hit_block_after_successful_hit(self):
        shot = Point(4, 5)
        self.player.ship_manager.ships_copy = [[Point(4, 5)]]
        self.player.check_is_successful_hit(shot)
        self.assertNotIn(shot, self.player.ship_manager.ships_set)

    def test_add_dotted_after_successful_hit(self):
        shot = Point(2, 3)
        self.player.update_dotted_and_hit(shot, diagonal_only=False)
        self.assertIn(Point(2, 2), self.player.dotted)

    def test_add_dotted_after_miss_2(self):
        shot = Point(6, 8)
        self.player.update_dotted_and_hit(shot, diagonal_only=False)
        self.assertIn(Point(6, 7), self.player.dotted)

    def test_no_change_in_dotted(self):
        shot = Point(0, -1)
        self.player.update_dotted_and_hit(shot, diagonal_only=False)
        self.assertFalse(self.player.dotted)

    def test_remove_hit_block_miss(self):
        shot = Point(4, 5)
        self.player.update_dotted_and_hit(shot, diagonal_only=True)
        self.assertIn(shot, self.player.hit_blocks)

    def test_add_dotted_after_miss(self):
        shot = Point(0, 0)
        self.player.update_dotted_and_hit(shot, diagonal_only=False)
        self.assertIn(Point(1, 1), self.player.dotted)

    def test_update_to_shot_after_shot(self):
        shot = Point(2, 3)
        self.player.update_dotted_and_hit(shot, diagonal_only=False)
        self.assertIn(shot, self.player.to_shot)

    def test_add_to_shot_after_successful_hit(self):
        shot = Point(2, 3)
        self.player.update_dotted_and_hit(shot, diagonal_only=False)
        self.assertIn(shot, self.player.to_shot)

    def test_remove_after_miss(self):
        shot = Point(4, 5)
        self.player.update_dotted_and_hit(shot, diagonal_only=False)
        self.assertIn(shot, self.player.to_shot)

    def test_add_to_injured_successful(self):
        self.player.ship_manager.ships_copy = [[Point(4, 5), Point(4, 6)], [Point(6, 7)]]
        shot = Point(2, 3)
        self.player.check_is_successful_hit(shot)
        self.assertNotIn(shot, self.player.injured)

    def test_successful_hit_without_destruction(self):
        shot = Point(2, 3)
        self.player.ship_manager.ships_copy = [[Point(2, 3)], [Point(4, 5)]]
        is_hit, is_destroyed = self.player.check_is_successful_hit(shot)
        self.assertTrue(is_hit)
        self.assertTrue(is_destroyed)
