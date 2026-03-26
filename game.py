from player import Player
from AI import AiAgent
from item import Item 
from npc import NPC
from location import Location

class Game:

    def __init__(self):
        self.player = Player()
        self.ai = AiAgent()
        self.locations = []
        self.game_active = False
        self.crime_committed = False

    def start_game(self):
        print("Welcome to the game!")
        choice = input("Do you want to commit a crime? (yes/no): ").lower()

        # If the player chooses yes, then they commit crime to start the game.
        if choice == "yes":
            self.commit_crime()
        else:
            print("You can't start without committing a crime.")

    def commit_crime(self):
        print("You committed a crime.")

        # Game is active and a crime has been committed to start the game.
        self.game_active = True
        self.crime_committed = True

    def create_game(self):
        kitchen = Location("Kitchen")
        bedroom = Location("Bedroom")
        garden = Location("Garden")
        garage = Location("Garage")
        living_room = Location("Living Room")
        office = Location("Office")

        # True evidences are required to win the game
        kitchen.items.append(Item("Knife", evidence=True))
        bedroom.items.append(Item("Secret Box", evidence=True))
        garage.items.append(Item("Gloves"))
        garden.items.append(Item("Shovel"))
        living_room.items.append(Item("Remote"))
        office.items.append(Item("Laptop"))

        kitchen.npcs.append(NPC("Chef"))
        bedroom.npcs.append(NPC("Maid"))
        garage.npcs.append(NPC("Guard"))
        garden.npcs.append(NPC("Gardener"))
        living_room.npcs.append(NPC("Guest"))
        office.npcs.append(NPC("Manager"))

        self.locations = [kitchen, bedroom, garage, garden, living_room, office]
        self.player.location = kitchen
