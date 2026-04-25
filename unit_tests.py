"""
This module is designed to contain the written unit tests for our code
"""
import unittest
from player import Player
from npc import NPC
from location import Location
from item import Item
from ai import AiAgent


class LocationUnitTests(unittest.TestCase):
    """A class to hold unit tests for the location class"""
    def setUp(self):
        self.loc = Location("Loc", "")

    def test_remove_item_not_present(self):
        """Test to verify locations can't remove items that aren't
        present"""
        temp_itm = Item("dummy Item", "", None)
        self.assertFalse(self.loc.remove_item(temp_itm))

    def test_add_npc(self):
        """Test to make sure a location can add npcs"""
        temp_npc = NPC("T", None)
        self.loc.add_npc(temp_npc)
        self.assertIn(temp_npc, self.loc.get_npcs())

    def test_remove_npc(self):
        """Test to make sure a location can remove npcs"""
        temp_npc = NPC("T", None)
        self.loc.add_npc(temp_npc)
        self.loc.remove_npc(temp_npc)
        self.assertNotIn(temp_npc, self.loc.get_npcs())

    def test_remove_npc_not_present(self):
        """Test to make sure a location is prevented from removing
        an npc who isn't there"""
        temp_npc = NPC("T", None)
        self.assertFalse(self.loc.remove_npc(temp_npc))

    def test_set_block_not_present(self):
        """Test to make sure that locations fail to set exits not in
        their list of exits"""
        self.assertFalse(self.loc.set_exit('S', None))


class NpcUnitTests(unittest.TestCase):
    """A class to hold unit tests for the npc class"""
    def setUp(self):
        self.loc = Location("Dummy loc", "")
        self.npc = NPC("A", self.loc)

    def test_location_getter(self):
        """Test to verify the location getter is functional"""
        self.assertIs(self.npc.get_location(), self.loc)

    def test_trust_getter(self):
        """Test to verify the trust getter is functional"""
        self.assertEqual(self.npc.trust_level(), 50)


class AiUnitTests(unittest.TestCase):
    """A class to hold unit tests for the AI class"""
    def setUp(self):
        temp_location = Location("Dummy location", "")
        temp_item = Item("dummyItem", "", location=temp_location)
        self.ai = AiAgent(incriminating_items_list=[temp_item],
                          start_location=Location("Dummy Location2", ""))

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
                          start_location=Location("Dummy Location2", ""))
        self.assertFalse(temp_ai.take_turn())


class PlayerUnitTests(unittest.TestCase):
    """A class to hold player unit tests"""
    def setUp(self):
        self.loc = Location("Dummy Loc", "")
        self.player = Player(self.loc)

    def test_get_sus_meter(self):
        """Test to see if the player's suspicion meter getter is functional"""
        self.assertEqual(self.player.get_suspicion(), 0)

    def test_use_consumable(self):
        """Test if using a consumable consumes it"""
        temp_item = Item("dummyItem", "", self.loc, consumable=True, required_location=self.loc)
        self.player.take_item(temp_item)
        self.player.use_item(temp_item)
        self.assertNotIn(temp_item, self.player.get_inventory())

    def test_not_in_inv_use(self):
        """Test that a player is prevented from using an item not in their inventory"""
        temp_item = Item("dummyItem", "", self.loc)
        self.assertFalse(self.player.use_item(temp_item))

    def test_not_in_inv_dispose(self):
        """Test that a player is prevented from disposing of an item not in their inventory"""
        temp_item = Item("dummyItem", "", self.loc)
        self.assertFalse(self.player.dispose_of_item(temp_item))


class PlayerLocationIntegrationTests(unittest.TestCase):
    """ A class to hold player/location integration tests"""
    def setUp(self):
        self.loc = Location("Dummy location", "")
        self.loc2 = Location("Dummy location 2", "", exits={self.loc: 1})
        self.loc.add_exit(self.loc2, 1)
        self.item = Item("dummyItem", "", location=self.loc)
        self.player = Player(self.loc)

    def test_player_takes(self):
        """Tests if player can take an item from a location and add it to their
        inventory"""
        self.player.take_item(self.item)
        self.assertIn(self.item, self.player.get_inventory())
        self.assertNotIn(self.item, self.loc.get_items())

    def test_player_fails_takes(self):
        """Tests if player is prevented from taking a blocked item"""
        temp_item = Item("dummyItem", "", location=self.loc, can_be_taken=False)
        self.assertFalse(self.player.take_item(temp_item))

    def test_player_moves(self):
        """Tests if a player can move between locations"""
        self.player.move_to(self.loc2)
        self.assertEqual(self.player.get_location(), self.loc2)

    def test_player_blocked(self):
        """Tests if a player is prevented from moving between blocked locations"""
        temp_loc = Location("Dummy Loc", "", exits={self.loc: 0})
        self.loc.add_exit(temp_loc, 0)
        failure = self.player.move_to(temp_loc)
        self.assertFalse(failure)

    def test_player_not_exit(self):
        """Test if a player is prevented from moving between non adjacent locations"""
        new_loc = Location("Dummy loc", "")
        self.assertFalse(self.player.move_to(new_loc))


class ItemLocationIntegrationTests(unittest.TestCase):
    """Checks if different classes interact correctly."""
    def setUp(self):
        self.room_a = Location("Room1", "Start")
        self.room_b = Location("Room2", "End")
        self.room_a.add_exit(self.room_b, 0)
        self.room_b.add_exit(self.room_a, 0)

    def test_unblock(self):
        """Tests if an item can be used to unblock a location"""
        key = Item("Key", "Key", self.room_a, required_location=self.room_a,
                   target_exit=self.room_b, effect_type="unblock")

        # This checks to see if key makes a door unblocked
        key.use(self.room_a)
        self.assertFalse(self.room_a.is_blocked(self.room_b))


if __name__ == '__main__':
    unittest.main()
