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

    def is_blocked(self):
        return self.blocked

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

    def add_exit(self, direction, location):
        self.exits[direction] = location

    def __str__(self):
        return f"{self.name}: {self.description}"
