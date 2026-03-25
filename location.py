class Location:
    def __init__(self, name, description, items=None, exits=None, npcs=None):
        self.name = name
        self.description = description
        self.items = items if items is not None else []
        self.exits = exits if exits is not None else {}
        self.npcs = npcs if npcs is not None else []


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

    def add_exit(self, location, blockState):
        self.exits[location] = blockState

    def add_mult_exit(self, exitDict={}):
        """Helper method that allows defining multiple exits simultaneously"""
        for exit in exitDict.keys():
            self.exits[exit] = exitDict[exit]

    def set_exit(self, exit, blockState):
        if blockState is None:
            blockState = 0
        
        if exit in self.exits:
            self.exits[exit] = blockState
        else:
            print(f"Error: {self.name} has no exit named {exit}")

    def __str__(self):
        return f"{self.name}: {self.description}"
