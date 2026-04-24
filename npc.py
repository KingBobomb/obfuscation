"""
This module provides a singular class for creating and maintaining an NPC.

Classes:
    NPC: Creates an NPC and manages its logic and data.
"""
import random


class NPC:
    """A class to create and manage an NPC.

    This class is designed to initialize an NPC and manage its logic for
    interacting with the Player and the AI about the locations of important
    items and the status of the suspicion meter

    Args:
        name (string): The NPC's name
        location (Location): The NPC's location
        ai_info (Item or None): An item that the AI can query the location of
    """
    def __init__(self, name, location, ai_info=None):
        """Initialization function for the npc class"""
        self.__name = name
        self.__location = location
        self.__ai_info = ai_info
        self.__trust = 50

    def get_location(self):
        """Getter for the NPC's location"""
        return self.__location

    def get_name(self):
        """Getter for the NPC's name"""
        return self.__name

    def get_info_ai(self):
        """Returns None or an item that the ai can query the location of."""
        return self.__ai_info

    def trust_level(self):
        """Returns the current trust level of the NPC."""
        return self.__trust

    def __get_responses(self, evidence_items):
        # Helper function to return a list of responses based on passed in item/items
        if evidence_items:
            return [
                f"I noticed something strange: {', '.join(evidence_items)} was here!",
                f"There seems to be {', '.join(evidence_items)} around.",
                f"I think {', '.join(evidence_items)} is important!"
            ]

        return [
            "I didn't notice anything unusual.",
            "Someone passed by earlier.",
            "I heard a strange noise."
        ]

    def has_talked_to(self, inventory, dialogue_choice):
        """A method used by the player to get a response from an NPC.

        This is a method that takes in a players inventory and their dialogue choice
        and prints a fitting message to the player.

        Arguments:
            inventory (list): The player's current inventory
            dialogue_choice (int): The dialogue response the player chose
        """
        # Evidence items that the player has.
        evidence_items = [item.get_name() for item in inventory if item.is_evidence()]

        print(f"You chose option: {dialogue_choice}")

        # If the player has an evidence item, then NPC gives a response.
        # The trust level is increases.
        if evidence_items:
            responses = self.__get_responses(evidence_items)
            print(f"{self.__name} says: {random.choice(responses)}")
            self.__trust = min(100, self.__trust + 5)
            return

        # Else, NPC will not talk to the player unless they have an evidence item.
        print(f"{self.__name} says: I won't talk unless you have something to show me.")
        return

    def __str__(self):
        return f"{self.__name}"
