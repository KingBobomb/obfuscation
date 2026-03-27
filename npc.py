import random

class NPC:
    def __init__(self, name, location, ai_info=None):
        """Initialize NPC with a name, location, ai_info and starting trust level."""
        self.name = name
        self.location = location
        self.ai_info = ai_info
        self.trust = 50

    def get_name(self):
        """Getter for the NPC's name"""
        return self.name

    def get_info_ai(self):
        """Returns None or an item that the ai can query the location of."""
        return self.ai_info
    
    def trust_level(self):
        """Returns the current trust level of the NPC."""
        return self.trust

    def get_responses(self, evidence_items):
        """Returns a list of possible responses based on the evidence items."""
        if evidence_items:
            return [
                f"I noticed something strange: {', '.join(evidence_items)} was here!",
                f"There seems to be {', '.join(evidence_items)} around.",
                f"I think {', '.join(evidence_items)} is important!"
            ]
        else:
            return [
                "I didn't notice anything unusual.",
                "Someone passed by earlier.",
                "I heard a strange noise."
            ]
    
    def has_talked_to(self, player):
        """NPC responds based on the evidence items in the player's inventory.
        Trust increases if the player has an evidence item."""
        # Evidence items that the player has.
        evidence_items = [item.name for item in player.inventory if item.evidence]

        # If the player has an evidence item, then NPC gives a response. 
        # The trust level is increases.
        if evidence_items:
            responses = self.get_responses(evidence_items)
            print(f"{self.name} says: {random.choice(responses)}")
            self.trust = min(100, self.trust + 5)
            return

        # Else, NPC will not talk to the player unless they have an evidence item.
        print(f"{self.name} says: I won't talk unless you have something to show me.")
        return
