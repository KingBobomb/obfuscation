class Player:
    def __init__(self):
        self.location = None
        self.inventory = []
        self.suspicion_meter = 0

    def travel(self, location):
        if location.blocked:
            print(f"{location.name} is blocked.")
        else:
            self.location = location
            print(f"You traveled to {location.name}.")

    def interact_location(self):
        if not self.location:
            print("You are not in a location.")
            return
        print(f"You are at {self.location.name}.")
        self.location.show_items()
        self.location.show_npcs()

    def take_item(self, index):
        if 0 <= index < len(self.location.items):
            item = self.location.items.pop(index)
            self.inventory.append(item)
            print(f"You picked up {item.name}.")

    def use_item(self, index):
        if 0 <= index < len(self.inventory):
            self.inventory[index].use()

    def dispose_item(self, index):
        if 0 <= index < len(self.inventory):
            item = self.inventory.pop(index)
            print(f"You disposed of {item.name}.")
            if item.evidence:
                print("Evidence removed. Suspicion may decrease!")

    def talk_to_npc(self, index):
        if 0 <= index < len(self.location.npcs):
            self.location.npcs[index].talk()

    def manipulate_npc(self, index):
        if 0 <= index < len(self.location.npcs):
            success = self.location.npcs[index].manipulate()
            if not success:
                self.suspicion_meter += 10
            else:
                self.suspicion_meter += 2 