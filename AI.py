def getNpcs(loc):
    """Temporary Function to simulate getting the list of NPCs at a location"""
    if loc == "kitchen":
        return ["Chef"]
    elif loc == "living room":
        return ["Maid", "Butler", "Guest1", "Guest2"]
    elif loc == "foyer":
        return["Guest3", "Guest4"]
    
def getFurniture(loc):
    """Temporary Function to simulate getting the list of furniture at a location"""
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

class AiAgent:
    """Template class for the AI agent."""
    def __init__(self, baseNpcWeight, baseSearchWeight, baseMoveWeight, startLocation):
        self.NpcWeight = baseNpcWeight
        self.searchWeight = baseSearchWeight
        self.moveWeight = baseMoveWeight

        self.currLoc = startLocation
        self.incriminatingItem1Loc = None
        self.incriminatingItem2Loc = None
        self.incriminatingItem3Loc = None

       
        self.NpcsInRoom = []
        self.NpcsSpokenTo = []

        self.furnitureInRoom = []
        self.furnitureSearched = []

        self.unblockedExits = []
        self.blockedExits = []
        self.updateRoomKnowledge()
        

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
                if i not in self.unblockedExits:
                    self.unblockedExits.append(i)
            else:
                self.blockedExits.append(i)
         


    
         