from location import Location
from item import Item
from npc import NPC
from ai import AiAgent

# Small home location for testing behavior with items and NPCs
kitchen = Location("Kitchen", "A kitchen with an open cutlery drawer.")
living_room = Location("Living room", "A living room with an end table"
                       " and a coat rack")
foyer = Location("Foyer", "Foyer")
basement = Location("Basement", "Basement")
outside = Location("Outside", "Outside")

kitchen.add_exit(living_room, 1)
living_room.add_mult_exit({kitchen: 1, foyer: 1, basement: 0})
foyer.add_mult_exit({living_room: 1, outside: 1})
basement.add_exit(living_room, 0)
outside.add_exit(foyer, 1)

knife = Item("Knife", "Knife", kitchen)
rollingPin = Item("Rolling Pin", "Rolling Pin", kitchen)
carKeys = Item("Car Keys", "Car Keys", living_room)
magazine = Item("Magazine", "Magazine", living_room)
spareChange = Item("Spare Change", "Spare Change", foyer)
basementKey = Item("Basement Key", "Basement Key",
                   foyer, required_location=living_room)
survey_footage = Item("Surveillance Footage", "Surveillance Footage",
                      basement, evidence=True)
gardenGnome = Item("Garden Gnome", "Garden Gnome", outside, False)
spareKey = Item("Spare Key", "Spare Key", outside)

kitchen.add_item(knife)
kitchen.add_item(rollingPin)
living_room.add_item(carKeys)
living_room.add_item(magazine)
foyer.add_item(spareChange)
foyer.add_item(basementKey)
basement.add_item(survey_footage)
outside.add_item(gardenGnome)
outside.add_item(spareKey)

chef = NPC("Chef", kitchen)
maid = NPC("Maid", living_room)
butler = NPC("Butler", living_room)
guest1 = NPC("Guest 1", foyer)
guest2 = NPC("Guest 2", foyer)
guest3 = NPC("Guest 3", outside)
guest4 = NPC("Guest 4", outside, survey_footage)

kitchen.add_npc(chef)
living_room.add_npc(maid)
living_room.add_npc(butler)
foyer.add_npc(guest1)
foyer.add_npc(guest2)
outside.add_npc(guest3)
outside.add_npc(guest4)

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
room1.add_mult_exit({room2: 1, room5: 1, room6: 1, room7: 1, })
room2.add_mult_exit({room1: 1, room3: 1, room7: 1, })
room3.add_mult_exit({room2: 1, room4: 1, })
room4.add_mult_exit({room3: 1, room9: 1, })
room5.add_mult_exit({room1: 1, room10: 0, })
room6.add_mult_exit({room1: 1, })
room7.add_mult_exit({room1: 1, room2: 1, room12: 1, })
room9.add_mult_exit({room4: 1, room10: 1, room14: 1, })
room10.add_mult_exit({room5: 0, room9: 1, room15: 1, })
room12.add_mult_exit({room7: 1, room13: 1, })
room13.add_mult_exit({room12: 1, room14: 1, room18: 0, })
room14.add_mult_exit({room9: 1, room13: 1, room15: 1, })
room15.add_mult_exit({room10: 1, room14: 1, })
room16.add_mult_exit({room21: 1, })
room18.add_mult_exit({room13: 0, room23: 1, })
room21.add_mult_exit({room16: 1, room22: 1, room25: 1, })
room22.add_mult_exit({room21: 1, room23: 1, })
room23.add_mult_exit({room18: 1, room22: 1, room24: 1, })
room24.add_mult_exit({room23: 1, room25: 1, })
room25.add_mult_exit({room24: 1, room21: 1, })

testAgent = AiAgent({'move': 1, 'search': 2, 'talk': 2},
                    living_room, [survey_footage])

for i in range(0, 50):
    testAgent.take_turn()

x = input("Press Enter to unlock basement")
living_room.set_exit(basement, 1)
basement.set_exit(living_room, 1)

ENDED = False

while not ENDED:
    ENDED = testAgent.take_turn()

print("Game Over")
