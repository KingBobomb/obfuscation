from player import Player
from investigator_ai import InvestigatorAI
from item import Item 
from npc import NPC
from location import Location

class Game:

    def __init__(self):
        self.player = Player()
        self.ai = InvestigatorAI()
        self.locations = []
        self.game_active = False
        self.crime_committed = False

    def start_game(self):
        print("Welcome to the game!")
        choice = input("Do you want to commit a crime? (yes/no): ").lower()

        if choice == "yes":
            self.commit_crime()
        else:
            print("You can't start without committing a crime.")

    def commit_crime(self):
        print("You committed a crime.")
        self.game_active = True
        self.crime_committed = True

    def create_game(self):
        kitchen = Location("Kitchen")
        bedroom = Location("Bedroom")
        garden = Location("Garden")
        garage = Location("Garage")

        kitchen.items.append(Item("Knife", evidence=True))
        bedroom.items.append(Item("Secret Box", evidence=True))
        garage.items.append(Item("Gloves"))
        garden.items.append(Item("Shovel"))

        kitchen.npcs.append(NPC("Chef"))
        bedroom.npcs.append(NPC("Maid"))
        garage.npcs.append(NPC("Guard"))
        garden.npcs.append(NPC("Gardener"))

        self.locations = [kitchen, bedroom, garage, garden]
        self.player.location = kitchen
    
    def win_game(self):
        
    def game_over(self):


