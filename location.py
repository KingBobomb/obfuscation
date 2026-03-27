class Location:
    def __init__(self, name, description, items=None, exits=None, npcs=None):
        self.name = name
        self.description = description
        self.items = items if items is not None else []
        self.exits = exits if exits is not None else {}
        self.npcs = npcs if npcs is not None else []

    def get_name(self):
        return self.name

    def get_items(self):
        return self.items

    def get_exits(self):
        return self.exits

    def get_npcs(self):
        return self.npcs

    def is_blocked(self, destination):
        # Check if the destination is an exit of this room, if not return false.
        if destination in self.exits:
            # If the exit to the user's destination is blocked
            # return true. Otherwise return false
            if self.exits[destination] == 0:
                return True
            else:
                return False
        else:
            return True

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
            return True
        return False

    def add_npc(self, npc):
        self.npcs.append(npc)

    def remove_npc(self, npc):
        #Remove an NPC from this location. Returns True if removed, False if not found.
        if npc in self.npcs:
            self.npcs.remove(npc)
            return True
        return False

    def add_exit(self, location, block_state):
        self.exits[location] = block_state

    def add_mult_exit(self, exit_dict):
        """Helper method that allows defining multiple exits simultaneously"""
        for exits in exit_dict.keys():
            self.exits[exits] = exit_dict[exits]

    def set_exit(self, new_exit, block_state):
        if block_state is None:
            block_state = 0

        if new_exit in self.exits:
            self.exits[new_exit] = block_state
        else:
            print(f"Error: {self.name} has no exit named {new_exit}")

    def __str__(self):
        return f"{self.name}: {self.description}"
