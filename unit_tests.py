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
    """A class to hold unit tests for the AI"""
    def setUp(self):
        temp_location= Location("Dummy location","")
        temp_item = Item("dummyItem", "", location=temp_location)
        self.ai = AiAgent(incriminating_items_list=[temp_item],
                          start_location=Location("Dummy Location2",""))

    def test_ai_get_suspicion(self):
        """Tests if getter for AI suspicion meter works."""
        ret = self.ai.get_suspicion_meter()
        self.assertIsInstance(ret, int)

    def test_ai_set_suspicion(self):
        """Tests if setter for AI suspicion meter works."""
        initial_sus = self.ai.get_suspicion_meter()
        self.ai.increment_suspicion_meter(20)
        self.assertEqual(initial_sus + 20, self.ai.get_suspicion_meter())

    def test_ai_suspicion_end_game(self):
        """Test if the AI will return false when the suspicion meter exceeds 100"""
        self.ai.increment_suspicion_meter(100)
        self.assertFalse(self.ai.take_turn())

    def test_ai_items_end_game(self):
        """Test if the AI will return false when there are no more incriminating items to find"""
        temp_ai = AiAgent(incriminating_items_list=[],
                          start_location=Location("Dummy Location2",""))
        self.assertFalse(temp_ai.take_turn())



class PlayerLocationIntegrationTests(unittest.TestCase):
    """ A class to hold player/location integration tests"""
    def setUp(self):
        self.loc= Location("Dummy location","")
        self.loc2=Location("Dummy location 2","",exits={self.loc: 1})
        self.loc.add_exit(self.loc2, 1)
        self.item = Item("dummyItem", "", location=self.loc)
        self.player = Player(self.loc)

    def test_player_takes(self):
        """Tests if player can take an item from a location and add it to their
        inventory"""
        self.player.take_item(self.item)
        self.assertIn(self.item, self.player.get_inventory())
        self.assertNotIn(self.item, self.loc.get_items())

    def test_player_moves(self):
        """Tests if a player can move between locations"""
        self.player.move_to(self.loc2)
        self.assertEqual(self.player.get_location(), self.loc2)

    def test_player_blocked(self):
        """Tests if a player is prevented from moving between blocked locations"""
        temp_loc = Location("Dummy Loc","",exits={self.loc : 0})
        self.loc.add_exit(temp_loc, 0)
        failure = self.player.move_to(temp_loc)
        self.assertFalse(failure)


class ItemLocationIntegrationTests(unittest.TestCase):
    """Checks if different classes interact correctly."""
    def setUp(self):
        self.room_a = Location("Room1", "Start")
        self.room_b = Location("Room2", "End")
        self.room_a.add_exit(self.room_b, 0)# blocked
        self.room_b.add_exit(self.room_a, 0)# blocked

    def test_unblock(self):
        """Tests if an item can be used to unblock a location"""
        key = Item("Key", "Key", self.room_a, required_location=self.room_a, 
                   target_exit=self.room_b, effect_type="unblock")

        # This checks to see if key makes a door unblocked
        key.use(self.room_a)
        self.assertFalse(self.room_a.is_blocked(self.room_b))



if __name__ == '__main__':
    unittest.main()
