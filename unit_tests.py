"""
This module is designed to contain the written unit tests for our code
"""
import unittest
from player import Player      
from npc import NPC             
from location import Location   
from Item import Item
from AI import AiAgent

class GameUnitTests(unittest.TestCase):
    """A class to hold unit tests for the ai, location and item"""
    def setUp(self):
        """basic game environment for every test."""
        self.hall = Location("Hall", "A hallway.")
        self.closet = Location("Closet", "A storage room.")
        
        # setting hallway and closet to be blocked
        self.hall.add_exit(self.closet, 0)
        self.closet.add_exit(self.hall, 0)
        
        self.player = Player(self.hall)
        self.evidence = Item("Evidence", "Dirty GLove", self.closet, evidence=True)
        
    def test_ai_suspicion(self):
        """Tests if the AI suspicion meter works."""
        ai = AiAgent(start_location=self.hall)
        ai.increment_suspicion_meter(20)
        self.assertEqual(ai.get_suspicion_meter(), 20)

    def test_location_exit_blocking(self):
        l1 = Location("L1", "Room 1")
        l2 = Location("L2", "Room 2")
        l1.add_exit(l2, 0) # 0 means blocked
        
        self.assertTrue(l1.is_blocked(l2), "Exit should be blocked")
        
        l1.set_exit(l2, 1) # 1 means unblocked
        self.assertFalse(l1.is_blocked(l2), "Exit should now be unblocked")

    def test_item_use_unblocks_path(self):
        """Tests if using an item unblocks an exit."""
        key = Item("Key", "Master key", self.hall, 
                   required_location=self.hall, 
                   target_exit=self.closet, 
                   effect_type="unblock")
        
        # See if it's blocked already
        self.assertTrue(self.hall.is_blocked(self.closet))
        
        # Use the item
        result = key.use(self.hall)
        
        # Assertions
        self.assertTrue(result)
        self.assertFalse(self.hall.is_blocked(self.closet), "Hall should be open")
        self.assertFalse(self.closet.is_blocked(self.hall), "Closet should be open")

    def test_player_inventory(self):
        """Tests if player can pick up an item"""
        item = Item("Flashlight", "So you can see", self.hall, can_be_taken=True)
        self.player.take_item(item)
        self.assertIn(item, self.player.get_inventory())

if __name__ == '__main__':
    unittest.main()
