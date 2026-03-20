class Player:
    def __init__(self):
        self.location = None
        self.inventory = []
        self.suspicion = 0

    def travel(self, new_location):
        if not self.location:
            self.location = new_location
            print(f"You start at {new_location.name}.")
            return

        # Check if destination is reachable
        if new_location in self.location.exits and self.location.exits[new_location] == 1:
            self.location = new_location
            print(f"You traveled to {new_location.name}.")
        else:
            print(f"You cannot go to {new_location.name} from here.")

    def interact_location(self):
        if not self.location:
            print("You are not in a location.")
            return
        print(f"\nYou are at {self.location.name}.")
        self.location.show_items()
        self.location.show_npcs()
        self.location.show_furniture()
        self.location.show_exits()

    def take_item(self, index):
        if 0 <= index < len(self.location.items):
            item = self.location.items.pop(index)
            self.inventory.append(item)
            print(f"You picked up {item.name}.")
        else:
            print("Invalid item.")

    def use_item(self, index):
        if 0 <= index < len(self.inventory):
            self.inventory[index].use()
        else:
            print("Invalid item.")

    def dispose_item(self, index):
        if 0 <= index < len(self.inventory):
            item = self.inventory.pop(index)
            print(f"You disposed of {item.name}.")

            if item.evidence:
                self.suspicion = max(0, self.suspicion - 10)
                print("Evidence removed. Suspicion decreased!")
        else:
            print("Invalid item.")

    def talk_to_npc(self, index):
        if 0 <= index < len(self.location.npcs):
            npc = self.location.npcs[index]
            npc.talk()
        else:
            print("Invalid NPC.")

    def manipulate_npc(self, index):
        if 0 <= index < len(self.location.npcs):
            npc = self.location.npcs[index]
            success = npc.manipulate()

            if not success:
                self.suspicion += 10
            else:
                self.suspicion += 2

            print(f"Your suspicion level: {self.suspicion}")
        else:
            print("Invalid NPC.")