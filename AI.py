import random

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
        return {"kitchen:": 1, "foyer": 1, "basement":0}
    elif loc == "foyer":
        return {"living room": 1, "outside":1}
    elif loc == "basement":
        return{"living room":0}
    elif loc == "outside":
        return{"foyer":1}

class AiAgent:
    """Template class for the AI agent."""
    def __init__(self, baseNpcWeight, baseSearchWeight, baseMoveWeight, startLocation, incriminatingItemsList):
        # Base weights for decision making tree
        self.NpcWeight = baseNpcWeight
        self.searchWeight = baseSearchWeight
        self.moveWeight = baseMoveWeight

        # AI starting location 
        self.currLoc = startLocation
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

        # Update values with info gathered from the current room
        self.updateRoomKnowledge()

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
         