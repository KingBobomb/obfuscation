import random
import collections
from location import Location

class AiAgent:
    """Template class for the AI agent."""
    def __init__(self, baseNpcWeight, baseSearchWeight, baseMoveWeight, startLocation, incriminatingItemsList):
        # Base weights for decision making tree
        self.NpcWeight = baseNpcWeight
        self.searchWeight = baseSearchWeight
        self.moveWeight = baseMoveWeight

        # AI starting location 
        self.currLoc = startLocation
        self.incriminatingItemFoundDict = {}
        # Collect data for each incriminating item passed in
        for item in incriminatingItemsList:
            self.incriminatingItemFoundDict[item] = 0
        
        # Initialize the Suspicion Meter
        self.suspicionMeter = 0
       
        # Initialize a list to keep track of NPCs in the current room of the AI
        self.NpcsInRoom = []
        # Initialize a list to keep track of the NPCs that the AI has currently spoken to
        self.NpcsSpokenTo = []

        # Initialize a list to keep track of furniture to search in the AI's current room.
        self.furnitureInRoom = []
        # Initialize a dictionary to keep track of the furniture the AI has searched and the room it's currently in
        self.furnitureSearched = []

        # Create a variable to contain the AI's knowledge of the map state.
        self.graph = None
        # Create an initial graph of the map, which will be updated as the AI finds previously blocked doors unblocked
        self.initializeGraph()
        # Update values with info gathered from the current room
        self.updateRoomKnowledge()

    def initializeGraph(self):
        """Method to create an initial graph of the map (so the AI doesn't instantly know about unblocked doors)"""
        # Queue for storing new nodes to visit. Note: Collection Module's deque is used to allow FIFO functionality efficiently
        nodeQueue = collections.deque([self.currLoc])
        # Set of already visited Nodes. Note: Set is used as it has a faster lookup time than a list.
        visitedNodes = {self.currLoc}
        # Initialize the AI's graph with the first location and its exits.
        self.graph = {self.currLoc:self.currLoc.get_exits()}
        while nodeQueue:
            currNode = nodeQueue.popleft()

            for node in currNode.get_exits().keys():
                if node not in visitedNodes:
                    nodeQueue.append(node)
            
            visitedNodes.add(currNode)
            self.graph[currNode] = currNode.get_exits()


    def getPathTo(self, targetLoc):
        """Method to get a pathway to a desired node in the AI's graph using BFS"""
        nodeQueue = collections.deque([self.currLoc])
        visitedNodes = [self.currLoc]
        predecessorNode = {self.currLoc: None}

        while nodeQueue:
            currNode = nodeQueue.popleft()

            if currNode == targetLoc:
                finalPath = []
                while predecessorNode[currNode] is not None:
                    finalPath.append(currNode)
                    currNode = predecessorNode[currNode]
                finalPath = finalPath[::-1]
                return finalPath

            currExits = self.graph[currNode]
            for node in currExits.keys():
                if node not in visitedNodes and currExits[node] != 0:
                    nodeQueue.append(node)
                    if node not in predecessorNode.keys():
                        predecessorNode[node] = currNode
            
            visitedNodes.append(currNode)
        
        return None


    def talkToNPC(self, chosenNPC):
        # Get information about incriminating items from the AI
        item = chosenNPC.getInfoAI()
        # Check if the NPC has informed the AI of an incriminating item
        if item is not None:
            # 
            item.getLocation()
        self.updateRoomKnowledge()

    def searchRoom(self, chosenSearchable):
         pass      

    def moveSelf(self, newLoc):
        if self.currLoc.is_blocked(newLoc):
            print(f"AI has attempted an invalid move from {self.currLoc.name} to {newLoc.name}")
        else:
            self.currLoc = newLoc
            self.updateRoomKnowledge()

    def updateRoomKnowledge(self):
        self.NpcsInRoom = self.currLoc.get_npcs()
        self.furnitureInRoom = self.currLoc.get_items()
        roomExits = self.currLoc.get_exits()

        if roomExits != self.graph[self.currLoc]:
            for exit in roomExits.keys():
                self.graph[self.currLoc][exit] = roomExits[exit]
                
         

    def takeTurn(self):
        # Check if the game should end, if so return true.
        if self.suspicionMeter >= 100:
            return True     


# Small home location for testing
kitchen = Location("Kitchen","Kitchen", ["knife","rolling pin",None], None, ["Chef"])
livingRoom = Location("Living room",None, ["car keys", "magazine", None], None, ["Maid", "Butler", "Guest1", "Guest2"])
foyer = Location("Foyer","Foyer", ["spare change","basement key",None], None, ["Guest3", "Guest4"])
basement = Location("Basement", "Basement", ["surveillance footage", None, None],None,None)
outside = Location("Outside", "Outside", ["Garden Gnome", "spare key"],None,None)

kitchen.add_exit(livingRoom, 1)
livingRoom.add_mult_exit({kitchen: 1, foyer: 1, basement:0})
foyer.add_mult_exit({livingRoom: 1, outside:1})
basement.add_exit(livingRoom,0)
outside.add_exit(foyer,1)

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

testAgent = AiAgent(1,1,1,room1,["surveillance footage"])

