class NPC:
    def __init__(self, name):
        self.name = name
        self.trust = 50

    def talk(self):
        responses = [
            "I didn't notice anything unusual.",
            "Someone passed by earlier.",
            "I heard a strange noise."
        ]
        print(f"{self.name} says: {random.choice(responses)}")

    def manipulate(self):
        success_chance = random.randint(0, 100) + self.trust // 2
        if success_chance > 60:
            print(f"{self.name} was convinced by your lie! You have manipulated an NPC.")
            return True
        else:
            print(f"{self.name} did not believe you. Suspicion increased!")
            return False