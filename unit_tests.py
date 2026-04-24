"""
This module is designed to contain the written unit tests for our code
"""
import unittest
from player import Player      
from npc import NPC             
from location import Location   
from Item import Item
from ai import AiAgent

class AiUnitTests (unittest.TestCase):
    """A class to hold unit tests for the ai"""
    def setUp(self):
        self.ai = AiAgent({'move': 1, 'search': 2, 'talk': 2})

class EnvironmentTests(unittest.TestCase):
    """ A class to hold unit tests for location and item """
    def test_location_exit_blocking(self):
        l1 = Location("L1", "Room 1")
        l2 = Location("L2", "Room 2")
        l1.add_exit(l2, 0) # 0 means blocked
        
        self.assertTrue(l1.is_blocked(l2), "Exit should be blocked")
        
        l1.set_exit(l2, 1) # 1 means unblocked
        self.assertFalse(l1.is_blocked(l2), "Exit should now be unblocked")

    def test_item_use_unblocks_path(self):
        hall = Location("Hall", "A hall")
        closet = Location("Closet", "A closet")
        hall.add_exit(closet, 0) # blocked
        closet.add_exit(hall, 0) # blocked
        
        key = Item("Key", "Key", hall, required_location=hall, 
                   target_exit=closet, effect_type="unblock")
        
        # Use the item
        key.use(hall)
        
        # Check if the location state changed
        self.assertFalse(hall.is_blocked(closet))
        self.assertFalse(closet.is_blocked(hall))

if __name__ == '__main__':
    unittest.main()
