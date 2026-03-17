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

        # FIX ME: Uncomment get functions as templates are fleshed out.
        # self.NpcsInRoom = startLocation.getNpcs()
        self.NpcsInRoom = getNpcs(startLocation)
        self.NpcsSpokenTo = []

        #self.furnitureInRoom = startLocation.getFurniture()
        self.furnitureInRoom = getFurniture(startLocation)
        self.furnitureSearched = []

        self.unblockedExits = []
        self.blockedExits = []
        #total exits = startLocation.getExits()
        totalExits = getExits(startLocation)

        for i in totalExits.keys():
            if totalExits[i] == 1:
                self.unblockedExits.append(i)
            else:
                self.blockedExits.append(i)
         


    
         