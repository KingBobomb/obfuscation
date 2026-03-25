import random
import collections
from location import Location
from item import Item

class AiAgent:
    """Template class for the AI agent."""
    def __init__(self, base_weights, start_location, incriminating_items_list):
        # Base weights for decision making tree
        self.npc_weight = base_weights[0]
        self.search_weight = base_weights[1]
        self.move_weight = base_weights[2]

        # AI starting location
        self.curr_loc = start_location

        # Dictionary for storing which Incriminating items the AI has found.
        self.incriminating_item_found_dict = {}
        # Dictionary for storing the location of each incriminating item the AI knows about.
        self.incriminating_item_location_dict = {}

        # Collect data for each incriminating item passed in
        for item in incriminating_items_list:
            self.incriminating_item_found_dict[item] = 0
            self.incriminating_item_location_dict = None

        # Initialize the Suspicion Meter
        self.suspicion_meter = 0

        # Initialize a list to keep track of NPCs in the current room of the AI
        self.npcs_in_room = []
        # Initialize a list to keep track of the NPCs that the AI has currently spoken to
        self.npcs_spoken_to = []

        # Initialize a list to keep track of furniture to search in the AI's current room.
        self.furniture_in_room = []
        # Initialize a list to keep track of the furniture the AI has searched
        self.furniture_searched = []

        # Create a variable to contain the AI's knowledge of the map state.
        self.graph = None
        # Create an initial graph of the map, updated as the AI learns of unblocked doors
        self.initialize_graph()
        # Update values with info gathered from the current room
        self.update_room_knowledge()

    def initialize_graph(self):
        """Method to create an initial graph of the map 
        (so the AI doesn't instantly know about unblocked doors)"""
        # Queue for storing new nodes to visit.
        node_queue = collections.deque([self.curr_loc])
        # Set of already visited Nodes.
        visited_nodes = {self.curr_loc}
        # Initialize the AI's graph with the first location and its exits.
        self.graph = {self.curr_loc:self.curr_loc.get_exits()}
        while node_queue:
            curr_node = node_queue.popleft()

            for node in curr_node.get_exits().keys():
                if node not in visited_nodes:
                    node_queue.append(node)

            visited_nodes.add(curr_node)
            self.graph[curr_node] = curr_node.get_exits()


    def get_path_to(self, target_loc):
        """Method to get a pathway to a desired node in the AI's graph using BFS"""
        node_queue = collections.deque([self.curr_loc])
        visited_nodes = [self.curr_loc]
        predecessor_node = {self.curr_loc: None}

        while node_queue:
            curr_node = node_queue.popleft()

            if curr_node == target_loc:
                final_path = []
                while predecessor_node[curr_node] is not None:
                    final_path.append(curr_node)
                    curr_node = predecessor_node[curr_node]
                final_path = final_path[::-1]
                return final_path

            curr_exits = self.graph[curr_node]
            for node in curr_exits.keys():
                if node not in visited_nodes and curr_exits[node] != 0:
                    node_queue.append(node)
                    if node in predecessor_node:
                        predecessor_node[node] = curr_node

            visited_nodes.append(curr_node)

        return None


    def talk_to_npc(self, chosen_npc):
        # Acknowledge when the AI attempts to speak to an NPC it has already spoken to.
        if chosen_npc in self.npcs_spoken_to:
            print("AI has attempted to speak to an AI it has already spoken to")
        else:
            # Add the chosen NPC to the list of NPCs the AI has already spoken to
            self.npcs_spoken_to.append(chosen_npc)
            # Get information about incriminating items from the AI
            item = chosen_npc.getInfoAI()
            # Check if the NPC has informed the AI of an incriminating item
            if item is not None:
                # Store the item in our list of incriminating items
                self.incriminating_item_location_dict[item] = item.get_location()
                print(f"{chosen_npc} has informed the AI of an incriminating item!")
            else:
                print(f"AI spoke to {chosen_npc}.")



    def search_room(self, chosen_searchable):
        pass

    def move_self(self, new_loc):
        # Acknowledge when the AI attempts to make an invalid move
        if self.curr_loc.is_blocked(new_loc):
            print(f"AI has attempted an invalid move from {self.curr_loc.name} to {new_loc.name}")
        else:
            self.curr_loc = new_loc
            print(f"AI has moved to {self.curr_loc.name}")
            self.update_room_knowledge()

    def update_room_knowledge(self):
        self.npcs_in_room = self.curr_loc.get_npcs()
        self.furniture_in_room = self.curr_loc.get_items()
        room_exits = self.curr_loc.get_exits()

        if room_exits != self.graph[self.curr_loc]:
            for exits in room_exits.keys():
                self.graph[self.curr_loc][exits] = room_exits[exits]


    def take_turn(self):
        # If the suspicion meter exceeds 100, end the game and return true.
        if self.suspicion_meter >= 100:
            return True

        # If the AI has found every incriminating item, end the game and return true
        if 0 not in self.incriminating_item_found_dict.values():
            return True

    def get_suspicion_meter(self):
        return self.suspicion_meter

    def increment_suspicion_meter(self, inc):
        self.suspicion_meter += inc

    def make_choice(self):
        pass

# Small home location for testing
kitchen = Location("Kitchen","Kitchen", [], None, ["Chef"])
livingRoom = Location("Living room",None, [], None, ["Maid", "Butler", "Guest1", "Guest2"])
foyer = Location("Foyer","Foyer", [], None, ["Guest3", "Guest4"])
basement = Location("Basement", "Basement", [],None,None)
outside = Location("Outside", "Outside", [],None,None)

kitchen.add_exit(livingRoom, 1)
livingRoom.add_mult_exit({kitchen: 1, foyer: 1, basement:0})
foyer.add_mult_exit({livingRoom: 1, outside:1})
basement.add_exit(livingRoom,0)
outside.add_exit(foyer,1)

knife = Item("Knife", "Knife", kitchen)
rollingPin = Item("Rolling Pin", "Rolling Pin", kitchen)
carKeys = Item("Car Keys", "Car Keys", livingRoom)
magazine = Item("Magazine", "Magazine", livingRoom)
spareChange = Item("Spare Change", "Spare Change", foyer)
basementKey = Item("Basement Key", "Basement Key", foyer, required_location=livingRoom)
survey_footage = Item("Surveillance Footage", "Surveillance Footage", basement, is_evidence=True)
gardenGnome = Item("Garden Gnome", "Garden Gnome", outside, False)
spareKey = Item("Spare Key", "Spare Key", outside)

kitchen.add_item(knife)
kitchen.add_item(rollingPin)
livingRoom.add_item(carKeys)
livingRoom.add_item(magazine)
foyer.add_item(spareChange)
foyer.add_item(basementKey)
basement.add_item(survey_footage)
outside.add_item(gardenGnome)
outside.add_item(spareKey)

# Large location for navigation testing
room1 = Location("Room 1", "Room 1")
room2 = Location("Room 2", "Room 2")
room3 = Location("Room 3", "Room 3")
room4 = Location("Room 4", "Room 4")
room5 = Location("Room 5", "Room 5")
room6 = Location("Room 6", "Room 6")
room7 = Location("Room 7", "Room 7")

room9 = Location("Room 9", "Room 9")
room10 = Location("Room 10", "Room 10")

room12 = Location("Room 12", "Room 12")
room13 = Location("Room 13", "Room 13")
room14 = Location("Room 14", "Room 14")
room15 = Location("Room 15", "Room 15")
room16 = Location("Room 16", "Room 16")

room18 = Location("Room 18", "Room 18")

room21 = Location("Room 21", "Room 21")
room22 = Location("Room 22", "Room 22")
room23 = Location("Room 23", "Room 23")
room24 = Location("Room 24", "Room 24")
room25 = Location("Room 25", "Room 25")

# Add exits (added after due to circular dependency)
room1.add_mult_exit({room2:1,room5:1,room6:1,room7:1,})
room2.add_mult_exit({room1:1,room3:1,room7:1,})
room3.add_mult_exit({room2:1,room4:1,})
room4.add_mult_exit({room3:1,room9:1,})
room5.add_mult_exit({room1:1,room10:0,})
room6.add_mult_exit({room1:1,})
room7.add_mult_exit({room1:1,room2:1,room12:1,})
room9.add_mult_exit({room4:1,room10:1,room14:1,})
room10.add_mult_exit({room5:0,room9:1,room15:1,})
room12.add_mult_exit({room7:1,room13:1,})
room13.add_mult_exit({room12:1, room14:1,room18:0,})
room14.add_mult_exit({room9:1,room13:1,room15:1,})
room15.add_mult_exit({room10:1,room14:1,})
room16.add_mult_exit({room21:1,})
room18.add_mult_exit({room13:0, room23:1,})
room21.add_mult_exit({room16:1,room22:1,room25:1,})
room22.add_mult_exit({room21:1,room23:1,})
room23.add_mult_exit({room18:1,room22:1,room24:1,})
room24.add_mult_exit({room23:1,room25:1,})
room25.add_mult_exit({room24:1,room21:1,})

testAgent = AiAgent([1,1,1],room1,["surveillance footage"])
