"""
This module provides a singular class for creating and maintaining an AI Agent.

Classes:
    AiAgent: Creates an AI Agent and manages its logic and collected data.
"""

from collections import deque
from random import choices


class AiAgent:
    """A class to create and manage an AI agent.

    This class is designed to initialize an AI Agent and
    manage its logic for taking its turn, moving around the map, gaining
    information from NPCs, searching for items, and ending the game.

    Args:
        base_weights (dict): Weights used to guide the AI on what to do during its turn
        start_location (Location): The starting location of the AI agent.
        incriminating_items_list (list): List of items the AI must find to win the game.
    """
    def __init__(self, base_weights=None, start_location=None, incriminating_items_list=None):
        # If base weights is none, set it to our default
        if base_weights is None:
            self.__base_weights = {'move': 1, 'search': 2, 'talk': 2}
        else:
            # Base weights for decision making tree
            self.__base_weights = base_weights

        # AI starting location
        self.__curr_loc = start_location
        # AI's previous three locations (used to prevent the AI from
        # revisiting locations too often)
        self.__prev_3_loc = deque([start_location])

        # Dictionary for storing which Incriminating items the AI has found.
        self.__incriminating_item_found_dict = {}
        # Stores the path to each incriminating item the AI knows about.
        self.__incriminating_item_path_dict = {}
        # Stores the location of each Incriminating item the AI knows about.
        self.__incriminating_item_loc_dict = {}

        # Collect data for each incriminating item passed in
        for item in incriminating_items_list:
            self.__incriminating_item_found_dict[item] = 0
            self.__incriminating_item_path_dict[item] = None
            self.__incriminating_item_loc_dict[item] = None

        self.__suspicion_meter = 0

        # Tracks NPCs in the current room of the AI it hasn't spoken to.
        self.__npcs_in_room = []
        # Tracks the NPCs that the AI has currently spoken to
        self.__npcs_spoken_to = []

        # Tracks items to search for in the AI's current room.
        self.__items_in_room = []
        # Tracks the items the AI has already found.
        self.__items_found = []

        # Tracks the number of interactions remaining at locations.
        self.__num_interactions = {}

        # Create a variable to contain the AI's knowledge of the map state.
        self.__graph = None
        # Create an initial graph of the map
        self.__initialize_graph()
        # Update values with info gathered from the current room
        self.__update_room_knowledge()

    def __initialize_graph(self):
        # Method to create an initial graph of the map separate from
        # the actual nodes so the AI doesn't instantly know about
        # unblocked doors

        # Queue for storing new nodes to visit.
        node_queue = deque([self.__curr_loc])
        # Set of already visited Nodes.
        visited_nodes = {self.__curr_loc}
        # Initialize the AI's graph with the first location and its exits.
        self.__graph = {self.__curr_loc: self.__curr_loc.get_exits()}
        while node_queue:
            curr_node = node_queue.popleft()

            # Calculate the number of interactions in a room.
            interactions = (len(curr_node.get_npcs())
                            + len(curr_node.get_items()))
            self.__num_interactions[curr_node] = interactions

            for node in curr_node.get_exits().keys():
                if node not in visited_nodes:
                    node_queue.append(node)

            visited_nodes.add(curr_node)
            self.__graph[curr_node] = curr_node.get_exits()

    def __get_path_to(self, target_loc):
        # Method to get a pathway to a desired node in the AI's graph using BFS
        # Unlike the initialize graph function, this runs on the AI's graph

        # Keeps track of the nodes to visit
        node_queue = deque([self.__curr_loc])
        # Keeps track of visited nodes
        visited_nodes = [self.__curr_loc]
        # Keeps track of the path we took to reach a node
        predecessor_node = {self.__curr_loc: None}

        # Run until there aren't any nodes to visit
        while node_queue:
            # Remove the first element of our queue
            curr_node = node_queue.popleft()

            # If we've reached our target destination, return the path back to our starting point
            if curr_node == target_loc:
                final_path = []
                while predecessor_node[curr_node] is not None:
                    final_path.append(curr_node)
                    curr_node = predecessor_node[curr_node]
                return final_path

            # Add new nodes to the queue and mark the current node as its predecessor
            curr_exits = self.__graph[curr_node]
            for node in curr_exits.keys():
                if node not in visited_nodes and curr_exits[node] != 0:
                    node_queue.append(node)
                    if node in predecessor_node:
                        predecessor_node[node] = curr_node

            visited_nodes.append(curr_node)

        # If no path is found to the given destination, return None
        return None

    def __talk_to_npc(self, chosen_npc):
        # Acknowledge when the AI attempts to speak to an NPC it has already spoken to.
        if chosen_npc in self.__npcs_spoken_to:
            print("AI has attempted to speak to an NPC it has already spoken to")
        else:
            # Add the chosen NPC to the list of NPCs the AI has already spoken to
            self.__npcs_spoken_to.append(chosen_npc)
            # Get information about incriminating items from the NPC
            item = chosen_npc.get_info_ai()
            # Check if the NPC has informed the AI of an incriminating item
            # Also check if the item is in our found items list, indicating the player took it.
            if item is not None and item.is_evidence() and item not in self.__items_found:
                # Store the item in our list of incriminating items
                self.__incriminating_item_loc_dict[item] = item.get_location()
                print(f"{chosen_npc.get_name()} has informed the AI of an incriminating item!")
            else:
                print(f"AI spoke to {chosen_npc.get_name()}.")

    def __search_room(self, search_choice):
        # Function to have an AI acknowledge an item like it's searching for it.

        # Acknowledge when the AI attempts to look for an item it has already found.
        if search_choice in self.__items_found:
            print("AI has attempted to search for an item it has already found")
        else:
            self.__items_found.append(search_choice)

            if search_choice in self.__incriminating_item_found_dict:
                self.__incriminating_item_found_dict[search_choice] = 1
                self.__incriminating_item_loc_dict[search_choice] = None
                self.__incriminating_item_path_dict[search_choice] = None
                print("The AI found an Incriminating Item")

            print(f"AI has found the item: {search_choice.get_name()}")

    def __move_self(self, new_loc):
        # Function to move the AI to a valid location specified by new_loc.

        # Acknowledge when the AI attempts to make an invalid move.
        if self.__curr_loc.is_blocked(new_loc):
            print("AI has attempted an invalid move from "
                  f"{self.__curr_loc.name} to {new_loc.get_name()}")
        else:
            if len(self.__prev_3_loc) == 3:
                # Remove the first element of the queue to keep the queue at 3 elements.
                self.__prev_3_loc.popleft()

            # Add the current location to the end of the queue
            self.__prev_3_loc.append(self.__curr_loc)
            # Move the AI to the new location.
            self.__curr_loc = new_loc
            print(f"AI has moved to {self.__curr_loc.get_name()}")

    def __update_room_knowledge(self):
        # Function to update the AI's knowledge of the room it's in.

        # Clear the current list of NPCs in the AI's current room.
        self.__npcs_in_room = []
        # Clear the list of items the AI hasn't found in the current room.
        self.__items_in_room = []

        # Add NPCs to our list of NPCs to talk to if we haven't spoken to them yet.
        for npc in self.__curr_loc.get_npcs():
            if npc not in self.__npcs_spoken_to:
                self.__npcs_in_room.append(npc)

        # Add items to our list of items to search for if we haven't found to them yet.
        for new_item in self.__curr_loc.get_items():
            if new_item not in self.__items_found:
                self.__items_in_room.append(new_item)

        # Update the remaining number of interactions at this location.
        interactions = len(self.__items_in_room) + len(self.__npcs_in_room)
        self.__num_interactions[self.__curr_loc] = interactions

        room_exits = self.__curr_loc.get_exits()

        # Check if a new exit is found that wasn't in our original graph
        if room_exits != self.__graph[self.__curr_loc]:
            # Update graph to match findings.
            for exits in room_exits.keys():
                self.__graph[self.__curr_loc][exits] = room_exits[exits]

            # Attempt to path to any items we couldn't before.
            for incrim_item, loc in self.__incriminating_item_loc_dict.items():
                if self.__incriminating_item_found_dict[incrim_item] != 1:
                    if loc is not None:
                        self.__incriminating_item_path_dict[incrim_item] = self.__get_path_to(loc)

    def take_turn(self):
        """Executes on turn cycle for the AI Agent and determines if the game should end.

        During its turn the AI will update it's knowledge of the room it's currently in,
        decide what action to take (between moving, talking to an NPC, or searching for an item),
        execute those actions, and check if the conditions are met to end the game.

        Returns:
            bool : True if the game should continue, false if the game should end
        """
        # Update the Ai's knowledge about the room its in.
        self.__update_room_knowledge()
        # Have the AI make a choice on what to do.
        self.__make_choice()

        # If the suspicion meter exceeds 100, end the game by returning false.
        if self.__suspicion_meter >= 100:
            return False

        # If the AI has found every incriminating item, end the game by returning false
        if 0 not in self.__incriminating_item_found_dict.values():
            return False

        # If neither are true, return true to continue the game.
        return True

    def get_suspicion_meter(self):
        """Getter method for the AI managed suspicion meter"""
        return self.__suspicion_meter

    def increment_suspicion_meter(self, inc):
        """Simple method to increment the AI managed suspicion meter by inc"""
        self.__suspicion_meter += inc

    def __handle_priority_behavior(self, item, loc):
        # Helper for the __make_choice function that checks and executes priority behaviors for
        # a given item. Returns true if a priority behavior was executed and false if not

        # Check if we know where an item is.
        if loc is None:
            return False

        # Check that we haven't already found the current item.
        if self.__incriminating_item_found_dict[item] == 1:
            return False

        # Check if we are in the same room as an incriminating item. If so, trigger a helper.
        if self.__curr_loc == loc:
            return self.__handle_incriminating_in_room(item)

        # Check if a pathway exists to our item. If so continue in that direction.
        if self.__incriminating_item_path_dict[item]:
            self.__move_self(self.__incriminating_item_path_dict[item][-1])
            self.__incriminating_item_path_dict[item].pop()
            return True

        return False

    def __handle_incriminating_in_room(self, item):
        # Helper for the __handle_priority_behavior function for when incriminating items are in
        # the same room as the AI

        # Check if there are any items left to search for in the current room.
        if not self.__items_in_room:
            # If an item should be here but isn't, we assume the player took it.
            # So we destroy the path and location of the item.
            self.__incriminating_item_loc_dict[item] = None
            self.__incriminating_item_path_dict[item] = None
            return False

        # Randomly search for an item in the room to emulate searching furniture
        to_search = choices(self.__items_in_room, k=1)[0]
        self.__search_room(to_search)
        return True

    def __make_choice(self):
        # Helper method to manage the logic for the AI's turn.

        move_mult = 1
        search_mult = 1
        talk_mult = 1

        # See if any priority behaviors need to occur for key items
        for incrim_item, loc in self.__incriminating_item_loc_dict.items():
            if self.__handle_priority_behavior(incrim_item, loc):
                return

        # If no predefined behavior was selected, adjust our weights for a
        # random selection
        # Note: Investigative style is intended to influence the move mult in
        # a later release

        # Talk mult is proportional to number of NPCs left to talk to in room.
        talk_mult = len(self.__npcs_in_room)
        # Search mult is proportional to number of items left in room.
        search_mult = len(self.__items_in_room)

        choice_weights = [self.__base_weights['move'] * move_mult,
                          self.__base_weights['search'] * search_mult,
                          self.__base_weights['talk'] * talk_mult]

        chosen = choices(list(self.__base_weights.keys()),
                         weights=choice_weights, k=1)[0]

        if chosen == 'move':
            # Weights are used to give a preference to moving towards
            # places with more interactions and not moving back to the
            # previous location.
            # Note: Like the graph, this is based on what the AI believes
            # about each location.
            room_weight_dict = {}

            # Add the number of interactions for each open exit
            for loc, block in self.__graph[self.__curr_loc].items():
                if loc in self.__prev_3_loc:
                    room_weight_dict[loc] = self.__num_interactions[loc] + 1
                elif block == 1:
                    room_weight_dict[loc] = self.__num_interactions[loc] + 4
                else:
                    room_weight_dict[loc] = 0
            if room_weight_dict:
                to_move = choices(list(room_weight_dict.keys()),
                                  weights=list(room_weight_dict.values()), k=1
                                  )[0]
                self.__move_self(to_move)
            else:
                print("The AI has no valid move to make.")
        elif chosen == 'search':
            # Randomly search for an item to emulate searching furniture
            to_search = choices(self.__items_in_room, k=1)[0]
            self.__search_room(to_search)
        else:
            # Randomly select an NPC in the room we haven't talked to
            to_talk = choices(self.__npcs_in_room, k=1)[0]
            self.__talk_to_npc(to_talk)

        return
