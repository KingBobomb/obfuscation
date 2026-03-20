import random

class NPC:
    def __init__(self, name):
        self.name = name
        self.trust = 50
        self.suspicion = 0
        self.has_info = False

    def talk(self, player):
        # Get the player's current location
        location = player.location

        # Check for evidence in this location
        evidence_items = [item.name for item in location.items if item.evidence]

        if evidence_items:
            responses = [
                f"I noticed something strange: {', '.join(evidence_items)} was here!",
                f"There seems to be {', '.join(evidence_items)} around.",
                f"I think {', '.join(evidence_items)} is important!"
            ]
        else:
            responses = [
                "I didn't notice anything unusual.",
                "Someone passed by earlier.",
                "I heard a strange noise."
            ]

        print(f"{self.name} says: {random.choice(responses)}")

        # Talking to an NPC increases trust.
        self.trust = min(100, self.trust + 5)


    def manipulate(self):
        success_chance = random.randint(0, 100) + (self.trust // 2)

        if success_chance > 60:
            print(f"{self.name} was convinced by your lie! You manipulated them.")
            self.trust = min(100, self.trust + 10)
            return True
        else:
            print(f"{self.name} did not believe you. Suspicion increased!")
            self.suspicion += 15
            return False