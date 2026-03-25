class Player:
    def __init__(self, start_location):
        self.inventory = []  # Stores items
        self.location = start_location  # Tracks current area
        self.suspicion_meter = 0  # Tracks player's risk of being caught

    def move_to(self, new_location):
        if new_location.is_unblocked:
            self.location = new_location
            return True
        return False

    def take_item(self, item):
        if item.can_be_taken:
            self.inventory.append(item)
            return True
        return False

    def use_item(self, item):
        if item in self.inventory:
            item.apply_effect()
            return True
        return False

    def dispose_of_item(self, item, disposal_set_piece):
        if item in self.inventory and disposal_set_piece.is_unblocked:
            self.inventory.remove(item)
            return True
        return False

    def interact_with_npc(self, dialogue_choice):
        if dialogue_choice == "suspicious":
            self.suspicion_meter += 10

    def manipulate_npc(self, npc):
        pass
