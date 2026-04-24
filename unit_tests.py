"""
This module is designed to contain the written unit tests for our code
"""
import unittest
from player import Player
from npc import NPC
from location import Location
from item import Item
from ai import AiAgent

class AiUnitTests(unittest.TestCase):
    """A class to hold unit tests for the ai"""
    def setUp(self):
        self.ai = AiAgent()

    def test_ai_get_suspicion(self):
        """Tests if getter for AI suspicion meter works."""
        ret = self.ai.get_suspicion_meter()
        self.assertIsInstance(ret, int)

    def test_ai_set_suspicion(self):
        """Tests if setter for AI suspicion meter works."""
        initial_sus = self.ai.get_suspicion_meter()
        self.ai.increment_suspicion_meter(20)
        self.assertEqual(initial_sus + 20, self.ai.get_suspicion_meter)

class item_tests(unittest.TestCase):
    """ Test to see if a player can pick up item"""
    def test_player_inventory(self):
        """Tests if player can pick up an item"""
        item = Item("Flashlight", "So you can see", self.hall, can_be_taken=True)
        self.player.take_item(item)
        self.assertIn(item, self.player.get_inventory())

class TestGameInteractions(unittest.TestCase):
    """Checks if different classes interact correctly."""
    def setUp(self):
        self.room_a = Location("Room1", "Start")
        self.room_b = Location("Room2", "End")
        self.room_a.add_exit(self.room_b, 0)# blocked
        self.room_b.add_exit(self.room_a, 0)# blocked

    def test_unblock(self):
        """Tests Item in location"""
        key = Item("Key", "Key", self.room_a, required_location=self.room_a, 
                   target_exit=self.room_b, effect_type="unblock")

        # This checks to see if key makes a door unblocked
        key.use(self.room_a)
        self.assertFalse(self.room_a.is_blocked(self.room_b))

    def test_movement(self):
        """Tests player and where it can and cannot go"""
        player = Player(self.room_a)
        # Verify player cannot move through blocked exit
        self.assertFalse(player.move_to(self.room_b))


if __name__ == '__main__':
    unittest.main()
