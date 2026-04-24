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
        """Initialization function for the player"""
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
            used_successfully = item.use(self.__location)

            # If it worked and the item is consumable remove it.
            if used_successfully and item.is_consumable():
                self.__inventory.remove(item)
                print(f"The {item.get_name()} was consumed.")

            return used_successfully

        return False

    def dispose_of_item(self, item):
        """Allows the player to dispose of an item using a valid disposal object.

        A method that takes in an item that the player wants to dispose of and disposes of it.
        Checks if the item is in their inventory and the given item is valid. If so it removes
        that Item from the player's inventory and returns True. Returns False if unsuccessful.

        Arguments:
            item (Item): The item the player is attempting to dispose of

        Returns:
            True if successful, False if unsuccessful
        """

        if item not in self.__inventory:
            return False

        # Remove item from inventory
        self.__inventory.remove(item)
        return True

    def interact_with_npc(self, dialogue_choice, chosen_npc):
        """A method designed to allow players to talk to NPCs

        This method takes in a dialog choice from a player and the NPC the player is interacting
        with, and communicates their choice to the NPC.

        Arguments:
            dialogue_choice (int): Player input integer specifying which dialog option they chose
            chosen_npc (NPC): The NPC the Player is currently interacting with

        """
        chosen_npc.has_talked_to(self.__inventory, dialogue_choice)
