import random
import collections

def getNpcs(loc):
    """Temporary Function to simulate getting the list of NPCs at a location"""
    if loc == "kitchen":
        return ["Chef"]
    elif loc == "living room":
        return ["Maid", "Butler", "Guest1", "Guest2"]
    elif loc == "foyer":
        return["Guest3", "Guest4"]
    
def getFurniture(loc):
    """Temporary Function to simulate getting the list of places to search at a location"""
    if loc == "kitchen":
        return ["Cabinet", "Oven", "Pantry"]
    elif loc == "living room":
        return ["Shelf", "Cabinet", "Under Couch"]
    elif loc == "foyer":
        return["Drawer"]
    
def getExits(loc):
    """Temporary Function to simulate getting a dict of exits at a location"""
    if loc == "kitchen":
        return {"living room": 1}
    elif loc == "living room":
        return {"kitchen": 1, "foyer": 1, "basement":0}
    elif loc == "foyer":
        return {"living room": 1, "outside":1}
    elif loc == "basement":
        return{"living room":0}
    elif loc == "outside":
        return{"foyer":1}
    elif loc == "Room 1":
        return{"Room 2":1,"Room 5":1,"Room 6":1,"Room 7":1,}
    elif loc == "Room 2":
        return{"Room 1":1,"Room 3":1,"Room 7":1,}
    elif loc == "Room 3":
        return{"Room 2":1,"Room 4":1,}
    elif loc == "Room 4":
        return{"Room 3":1,"Room 9":1,}
    elif loc == "Room 5":
        return{"Room 1":1,"Room 10":0,}
    elif loc == "Room 6":
        return{"Room 1":1,}
    elif loc == "Room 7":
        return{"Room 1":1,"Room 2":1,"Room 12":1,}
    elif loc == "Room 9":
        return{"Room 4":1,"Room 10":1,"Room 14":1,}
    elif loc == "Room 10":
        return{"Room 5":0,"Room 9":1,"Room 15":1,}
    elif loc == "Room 12":
        return{"Room 7":1,"Room 13":1,}
    elif loc == "Room 13":
        return{"Room 12":1, "Room 14":1,"Room 18":0,}
    elif loc == "Room 14":
        return{"Room 9":1,"Room 13":1,"Room 15":1,}
    elif loc == "Room 15":
        return{"Room 10":1,"Room 14":1,}
    elif loc == "Room 16":
        return{"Room 21":1,}
    elif loc == "Room 18":
        return{"Room 13":0, "Room 23":1,}
    elif loc == "Room 21":
        return{"Room 16":1,"Room 22":1,"Room 25":1,}
    elif loc == "Room 22":
        return{"Room 21":1,"Room 23":1,}
    elif loc == "Room 23":
        return{"Room 18":1,"Room 22":1,"Room 24":1,}
    elif loc == "Room 24":
        return{"Room 23":1,"Room 25":1,}
    elif loc == "Room 25":
        return{"Room 24":1,"Room 21":1,}
    

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
        #self.updateRoomKnowledge()

    def initializeGraph(self):
        """Method to create an initial graph of the map (so the AI doesn't instantly know about unblocked doors)"""
        nodeQueue = collections.deque([self.currLoc])
        visitedNodes = [self.currLoc]
        newGraph = {self.currLoc:getExits(self.currLoc)}
        while nodeQueue:
            currNode = nodeQueue.popleft()

            for node in getExits(currNode).keys():
                if node not in visitedNodes:
                    nodeQueue.append(node)
            
            visitedNodes.append(currNode)
            newGraph[currNode] = getExits(currNode)

        self.graph = newGraph

    def getPathTo(self, targetLoc):
        """Method to test if a pathway exists to the desired location in the AI's graph using BFS"""
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
        self.currLoc = newLoc
        self.updateRoomKnowledge()

    def updateRoomKnowledge(self):
        # FIX ME: Uncomment get functions as templates are fleshed out.
        # self.NpcsInRoom = self.currLoc.getNpcs()
        self.NpcsInRoom = getNpcs(self.currLoc)
        #self.furnitureInRoom = self.currLoc.getFurniture()
        self.furnitureInRoom = getFurniture(self.currLoc)
        #total exits = self.currLoc.getExits()
        roomExits = getExits(self.currLoc)

        for i in roomExits.keys():
            if roomExits[i] == 1:
                if i in self.blockedExits:
                    self.blockedExits.remove(i)
                    if i in self.incriminatingItemsDict.keys():
                        self.incriminatingItemsDict[i] = 1
                if i not in self.unblockedExits:
                    self.unblockedExits.append(i)
            else:
                self.blockedExits.append(i)
         

    def takeTurn(self):
        # Check if the game should end, if so return true.
        if self.suspicionMeter >= 100:
            return True     


testAgent = AiAgent(1,1,1,"Room 1",["knife"])
print(testAgent.graph)
print()
print(testAgent.getPathTo("Room 15"))
# Desynchronizing AI graph from actual graph for testing purposes
testAgent.graph["Room 5"]["Room 10"] = 1
testAgent.graph["Room 10"]["Room 5"] = 1

print(testAgent.getPathTo("Room 15"))