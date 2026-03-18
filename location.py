class Location:
    def __init__(self, name):
        self.name = name
        self.items = []
        self.npcs = []
        self.blocked = False

    def show_items(self):
        if not self.items:
            print("No items here.")
        else:
            print("Items in this location:")
            for idx, item in enumerate(self.items, 1):
                print(f"{idx}. {item.name} {'(Evidence)' if item.evidence else ''}")

    def show_npcs(self):
        if not self.npcs:
            print("No NPCs here.")
        else:
            print("NPCs here:")
            for idx, npc in enumerate(self.npcs, 1):
                print(f"{idx}. {npc.name}")
