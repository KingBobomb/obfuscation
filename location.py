class Location:
    def __init__(self, name):
        self.name = name
        self.items = []
        self.npcs = []
        self.furniture = []
        self.exits = {}

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
    
    def show_furniture(self):
        if not self.furniture:
            print("No furniture here.")
        else:
            print("Furniture here:")
            for idx, furn in enumerate(self.furniture, 1):
                print(f"{idx}. {furn}")

    def show_exits(self):
        if not self.exits:
            print("No exits.")
        else:
            print("Exits:")
            for loc, status in self.exits.items():
                state = "open" if status == 1 else "blocked"
                print(f"- {loc.name} ({state})")
