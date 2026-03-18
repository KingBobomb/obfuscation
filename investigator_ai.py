import random

class InvestigatorAI:
    def __init__(self):
        self.progress = 0
        self.style = random.choice(["evidence", "interrogation", "exploration"])

    def investigate(self, player):
        action = ""
        if self.style == "evidence":
            action = "search location"
            self.progress += self.search_evidence(player)
        elif self.style == "interrogation":
            action = "interrogate NPC"
            self.progress += self.question_npc(player)
        else:
            action = "explore location"
            self.progress += self.explore(player)
        print(f"AI investigator action: {action}. Investigation progress: {self.progress}")

    def search_evidence(self, player):
        found = random.choice([0, 1])
        if found and any(item.evidence for item in player.inventory):
            print("AI may have noticed missing evidence!")
            return 1
        return 0

    def question_npc(self, player):
        npc_count = len(player.location.npcs) if player.location else 0
        if npc_count > 0:
            print("AI questioned an NPC at your location.")
            return 1
        return 0

    def explore(self, player):
        if random.choice([0, 1]):
            print("AI explored and found some clues.")
            return 1
        return 0
