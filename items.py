"""
This module provides a singular class for creating and maintaining an Item.

Classes:
    Item: Creates an Item and manages its logic and data.
"""


class Item:
    """A class to create and manage an Item.

    This class is designed to initialize an Item and manage it's data,
    including whether or not it's a key item, the location of the item,
    where the item can be used, if the item can be picked up, the item's
    name and the item's description.

    Args:
        name (string): The item's name
        description (string): The item's description
        location (Location): The current location of the Item.
        can_be_taken (bool): Specifies if the player can pick up the item (default = True)
        evidence (bool): Specifies if the item is a key item (default = False)
        required_location (Location): Specifies the location where the item can be used
        container (string): Name of the container the item is in.
        block_msg (string): Message to display when an attempt to pick up the item fails
        unblock_item (Item or None): The item required to unblock this item
        exit_to_unblock (Location or None): The exit this item unblocks
    """
    def __init__(self, name, description, location,
                 can_be_taken = True, evidence = False, required_location = None,
                 container="", block_msg="", unblock_item = None, exit_to_unblock = None):
        self.__name = name
        self.__description = description
        self.__location = location
        self.__can_be_taken = can_be_taken
        self.__evidence = evidence
        self.__required_location = required_location
        self.__container = container
        self.__block_msg = block_msg
        self.__unblock_item = unblock_item
        self.__exit_to_unblock = exit_to_unblock

    def get_name(self):
        """Getter method for the Item's name"""
        return self.__name

    def get_container(self):
        """Getter method for the Item's container"""
        return self.__container

    def get_unblock_item(self):
        """Getter method for the Item's unblock item"""
        return self.__unblock_item

    def get_block_msg(self):
        """Getter for the Item's block message"""
        return self.__block_msg

    def get_exit_to_unblock(self):
        """Getter for the exit this item unblocks"""
        return self.__exit_to_unblock

    def can_be_taken(self):
        """Method to check if an item can be picked up"""
        return self.__can_be_taken

    def is_evidence(self):
        """Method to check if an item is a key item"""
        return self.__evidence

    def get_location(self):
        """Getter method for the item's current location"""
        return self.__location

    def set_unblock_item(self, unblock_item):
        """Setter method for the Item's unblock Item"""
        self.__unblock_item = unblock_item

    def set_exit_to_unblock(self, exit_to_unblock):
        """Setter method for the exit this item unblocks"""
        self.__exit_to_unblock = exit_to_unblock

    def use(self, current_location):
        """Method to allow the caller to use an item.

        This method takes in a location, checks if the item can
        be used there, and applies the Item's effect.

        Arguments:
            current_location (Location): The caller's current Location

        Returns:
            True if the item was successfully used, False if not.

        Notes:
            This method is currently incomplete for this release as
            the apply_effect helper function still needs to be implemented.
        """
        # Check if the item requires a specific location to be used
        if self.__required_location and current_location != self.__required_location:
            print(
                f"The {self.__name} can't be used here. "
                f"You need to be in the {self.__required_location}."
            )
            return False

        print(f"You used the {self.__name}: {self.__description}")
        self.__apply_effect()
        return True

    def __apply_effect(self):
        # Unimplemented helper function for actually using an item
        pass
