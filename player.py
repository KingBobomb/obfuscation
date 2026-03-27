"""
This module provides a singular class for creating and maintaining a player.

Classes:
    Player: Creates a Player and manages its logic and data.
"""


class Player:
    """A class to create and manage a Player.

    This class is designed to initialize a player and
    manage its logic for taking its turn, moving around the map, interacting
    with from NPCs, searching for items, and ending the game.

    Args:
        start_location (Location): The initial starting location of the Player
    """
    def __init__(self, start_location):
        self.__inventory = []  # Stores items
        self.__location = start_location  # Tracks current area
        self.__suspicion_meter = 0  # Tracks player's risk of being caught

    def get_inventory(self):
        """Getter for the Player's inventory"""
        return self.__inventory

    def get_location(self):
        """Getter for the player's current location"""
        return self.__location

    def get_suspicion(self):
        """Getter for the player managed suspicion meter"""
        return self.__suspicion_meter

    def move_to(self, new_location):
        """A method to move the player to a new location

        This method takes in a location the player wishes to move to,
        tests if the movement is valid, and either moves the player there
        and returns true for valid movement or returns false for invalid
        movement.

        Arguments:
            new_location (Location): The location the player wishes to move to

        Returns:
            True if the movement is successful, False if the movement was invalid
        """
        if not new_location.is_blocked(self.__location):
            self.__location = new_location
            return True
        return False

    def take_item(self, item):
        """A method to allow the player to add items to their inventory

        This method takes in an item that the player wants to take, checks
        if it is valid to take that item, and adds that item to the player's
        inventory. Returns True if successful, and False if unsuccessful

        Arguments:
            item (Item): The item the player is attempting to take

        Returns:
            True if taking the item is successful, False if taking the item is invalid
        """
        if item.can_be_taken():
            self.__inventory.append(item)
            return True
        return False

    def use_item(self, item):
        """A method to allow the player to use items in their inventory

        This method takes in an item that the player wants to use, checks
        if it is in their inventory, and calls that Item's use function.
        Returns True if successful, and False if unsuccessful

        Arguments:
            item (Item): The item the player is attempting to use

        Returns:
            True if using the item is successful, False if using the item is invalid
        """
        if item in self.__inventory:
            return item.use(self.__location)
        return False

    def dispose_of_item(self, item, disposal_set_piece):
        """A currently incomplete method designed to allow players to dispose of items

        This is a currently incomplete method that takes in an item that the player wants
        to dispose of and an object that the want to use to dispose it, checks if the item
        is in their inventory and the disposal object is unblocked, and removes that Item's
        from the player's inventory. Returns True if successful, and False if unsuccessful

        Arguments:
            item (Item): The item the player is attempting to use
            disposal_set_piece (Object): The object used to dispose of the Item

        Returns:
            True if using the item is successful, False if using the item is invalid

        Notes:
            As of this release this function is unfinished as there are still ongoing
            discussions about whether the disposal object should be an instance of
            Item/Location or if there is enough specific behavior to warrant a unique
            class.
        """
        if item in self.__inventory and disposal_set_piece.is_unblocked:
            self.__inventory.remove(item)
            return True
        return False

    def interact_with_npc(self, dialogue_choice, chosen_npc):
        """A currently incomplete method designed to allow players to talk to NPCs

        This method is a currently incomplete method that takes in a dialog choice
        from a player and the NPC the player is interacting with, and communicates
        them to an NPC.

        Arguments:
            dialogue_choice (int): Player input integer specifying which dialog option they chose
            chosen_npc (NPC): The NPC the Player is currently interacting with

        Notes:
            As of this release, this function is unfinished as there are still ongoing
            discussions about how to handle communication between the player, game, and
            NPC classes and disagreements on logic distribution.
        """
        chosen_npc.has_talked(self.__inventory, dialogue_choice)

        # FIX ME: Decide encapsulation for dialogue_choice
        # (potentially let the NPC class handle this logic)
        # if dialogue_choice == "suspicious":
        #     self.__suspicion_meter += 10

    def manipulate_npc(self, npc):
        """A currently unimplemented method designed to allow players to manipulate NPCs

        This method is a currently unimplemented method that takes in the NPC the player
        is interacting with and communicating with the NPC class to determine the result
        of the attempted manipulation.

        Arguments:
            npc (NPC): The NPC the player is currently interacting with

        Notes:
            As of this release, this function still needs to be implemented. Additionally,
            there are still ongoing discussions about how to handle communication between
            the player, and NPC classes, and disagreements on logic distribution.
        """
        # FIX ME: Implement class (further discussion on NPC to
        # player communications and distribution of logic required)
        print(npc)
