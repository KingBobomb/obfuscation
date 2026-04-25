"""
This module provides a singular class for creating and maintaining a Location.

Classes:
    Location: Creates a Location and manages its data.
"""


class Location:
    """A class to create and manage a Location.

    This class is designed to initialize a Location and to keep track
    of the items and Npcs stored there and the locations that can be
    reached from this location (exits).

    Args:
        name (string): Name of the given location
        description (string): The description of the given location
        items (list or None): The list of items at the given location.
        exits (dict or None): A dictionary of the location's exits and
            their block state
        npcs (list or None): The list of npcs at the given location.
    """
    def __init__(self, name, description, items=None, exits=None, npcs=None):
        """Initialization function for the location"""
        self.__name = name
        self.__description = description
        self.__items = items if items is not None else []
        self.__exits = exits if exits is not None else {}
        self.__npcs = npcs if npcs is not None else []

    def get_name(self):
        """Getter method for the location's name"""
        return self.__name

    def get_items(self):
        """Getter method for the location's list of items"""
        return self.__items

    def get_exits(self):
        """Getter method for the location's dict of exits"""
        return self.__exits

    def get_npcs(self):
        """Getter method for the location's list of NPCs"""
        return self.__npcs

    def is_blocked(self, destination):
        """Method to determine if movement to a location is blocked.

        This method takes in a location specified by destination and checks
        if a movement to this location is invalid. If a movement is invalid
        this method returns True. If a movement is valid, this method returns
        False.

        Arguments:
            destination (Location): Specifies where the caller wants to move to

        Returns:
            True if the movement is invalid, False if the movement is valid.

        """
        # Check if the destination is an exit of this room, if not return True.
        if destination in self.__exits:
            # If the exit to the user's destination is blocked
            # return true. Otherwise return false
            if self.__exits[destination] == 0:
                return True
            else:
                return False
        else:
            return True

    def add_item(self, item):
        """Method to add an item to the location's list of items."""
        self.__items.append(item)

    def remove_item(self, item):
        """Method to remove an item from a location.
        Returns True if removed, False if the item was not found."""
        if item in self.__items:
            self.__items.remove(item)
            return True
        return False

    def add_npc(self, npc):
        """Method to add an NPC to the location's list of NPCs."""
        self.__npcs.append(npc)

    def remove_npc(self, npc):
        """Method to remove an NPC from a location.
        Returns True if removed, False if the NPC was not found."""
        if npc in self.__npcs:
            self.__npcs.remove(npc)
            return True
        return False

    def add_exit(self, location, block_state):
        """A method to add an exit to our location's list of exits

        This method takes in a Location and an integer specifying whether
        the location is blocked (0) or not (1) and adds it to the calling
        location's dictionary of exits.

        Arguments:
            location (Location): A location to add to our list of exits
            block_state (int): An int specifying if the location is blocked
        """
        self.__exits[location] = block_state

    def add_mult_exit(self, exit_dict):
        """A method that allows defining multiple exits simultaneously

        This method is intended to be used when adding individual exits to a
        location would be too slow or tedious. It takes in a dictionary of
        Location and int pairs and adds them to the location's list of exits.

        Arguments:
            exit_dict (dict): A dictionary of Location and block state pairs

        """
        for exits in exit_dict.keys():
            self.__exits[exits] = exit_dict[exits]

    def set_exit(self, exit_to_alter, block_state):
        """Setter function used to alter whether an exit is blocked or not.

        This method takes in a location specified by exit_to_alter and checks if it
        is an exit to the current location. If it is, we set the block state of
        the exit to the int passed in by block_state and return true. If it isn't,
        we print a message indicating that the set attempt failed and return false.

        Arguments:
            exit_to_alter (Location): An exit of the current location to alter
            block_state (int): Value to set the chosen exit's block state to

        """
        if block_state is None:
            block_state = 0

        if exit_to_alter in self.__exits:
            self.__exits[exit_to_alter] = block_state
            return True
        else:
            print(f"Error: {self.__name} has no exit named {exit_to_alter}")
            return False

    def __str__(self):
        return f"{self.__name}: {self.__description}"
