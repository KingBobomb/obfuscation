"""
This module provides a singular class for creating and maintaining a Game.

Classes:
    Game: Creates a Game and manages its logic and data.
"""
from player import Player
from ai import AiAgent
from items import Item
from npc import NPC
from location import Location


class Game:
    """A class to create and manage a Game.

    This class is designed to initialize a game and manage its logic, such
    as controlling whose turn it is, getting user input, and ending the game
    when necessary.
    """
    def __init__(self):
        player, ai = self.__create_game()
        self.__player = player
        self.__ai = ai
        self.__locations = []
        self.__game_active = False

    def get_locations(self):
        """Getter function for the list of locations in the game"""
        return self.__locations

    def start_game(self):
        """A method to prompt the user to start the game

        This method prompts the user for a response. If the user's response
        is yes, then we begin running the game. If the user's response is no,
        we print out a failure message.
        """
        print("Welcome to the game!")
        choice = input("Do you want to commit a crime? (yes/no): ").lower()

        # If the player chooses yes, then they commit crime to start the game.
        if choice == "yes":
            self.__commit_crime()
        else:
            print("You can't start without committing a crime.")

    def __prompt_user(self):
        # Helper method to obtain user input

        # Obtain player location
        player_loc = self.__player.get_location()

        print(f"Current location - {player_loc}")

        player_turn = True
        # Function references the player can choose from
        action_list = [self.__handle_player_move, self.__handle_player_speak,
                       self.__handle_player_use, self.__handle_player_dispose]

        while player_turn:
            print("\nPlease enter the number of the option you'd like to select:")
            print("1 - Move to a new room")
            print("2 - Speak with someone in the room")
            print("3 - Use an item")
            print("4 - Dispose of an item")

            player_response = input().strip().lower()

            if player_response == 'back':
                player_response = "back to where?"

            valid_check, end_game = self.__validate_input(4, player_response)

            if end_game:
                return False

            if valid_check > 0:
                player_turn, end_game = action_list[valid_check - 1](player_loc)

            if end_game:
                return False

        return True

    def __handle_player_move(self, player_loc):
        # Helper function to handle the player moving. Returns a tuple where
        # the first value is a bool indicating if the move was successful and
        # the second value is a bool indicating if the player wants to end the
        # game.
        loc_exits = player_loc.get_exits()
        end_game = False

        if len(loc_exits) == 0:
            print("\nThere are no valid locations to move to.")
            return False, end_game

        valid = False

        while not valid:
            print("\nSelect a location to move to or type 'back' to go back:")
            for i, ext in enumerate(loc_exits):
                print(f"{i + 1} - {ext}")

            player_choice = input().strip().lower()
            validity_check, end_game = self.__validate_input(len(loc_exits),player_choice)

            if end_game:
                return False, end_game

            if validity_check == 0:
                return True, end_game

            if validity_check > 0:
                chosen_exit = list(loc_exits.keys())[validity_check - 1]

                if player_loc.is_blocked(chosen_exit):
                    print("\nThis location is blocked. "
                    "Use an item to unblock it or select another location.")
                else:
                    if self.__player.move_to(chosen_exit):
                        print(f"Moved to {chosen_exit.get_name()}")
                        valid = True
                    else:
                        print(f"Movement to {chosen_exit.get_name()} failed.")

        return False, end_game

    def __handle_player_speak(self):
        return False

    def __handle_player_use(self):
        return False

    def __handle_player_dispose(self):
        return False

    def __validate_input(self, upper_bound, player_response):
        # Helper function to validate a user's input. Returns a tuple where the
        # first value is -1 if invalid, 0 if an accepted word is detected/the
        # player attempts to end the game, and the player's response as an int
        # if valid, and the second value is true if the player wants to end the
        # game and false if not.

        if upper_bound == 1:
            ext_msg = "Please enter 1 to make this selection."
        else:
            ext_msg = f"Please enter a number between 1 and {upper_bound} to make a selection."

        if player_response in ['exit', 'quit']:
            print("Ending game...")
            return (0, True)

        if player_response == 'back':
            return (0, False)

        if not player_response.isnumeric():
            print("\nSorry, I didn't understand.")
            print(ext_msg)
            return (-1, False)

        selected = int(player_response)

        if 1 <= selected <= upper_bound:
            return (selected, False)

        print("\nSorry, I didn't understand.")
        print(ext_msg)
        return (-1, False)


    def __commit_crime(self):
        # Helper method to actually activate the game
        print("You committed a crime.")
        print("Type exit or quit to end the game at any point.\n")

        # Game is active and a crime has been committed to start the game.
        self.__game_active = True
        self.__run_game()

    def __run_game(self):
        # Helper method that contains the game loop
        while self.__game_active:
            self.__game_active = self.__prompt_user()

            if self.__game_active:
                print()
                self.__game_active = self.__ai.take_turn()

    def __create_game(self):
        # Helper method to initialize game objects
        kitchen = Location("Kitchen", "A kitchen with an open cutlery drawer.")
        living_room = Location("Living room", "A living room with an end table and a coat rack")
        foyer = Location("Foyer", "Foyer")
        basement = Location("Basement", "Basement")
        outside = Location("Outside", "Outside")

        kitchen.add_exit(living_room, 1)
        living_room.add_mult_exit({kitchen: 1, foyer: 1, basement: 0})
        foyer.add_mult_exit({living_room: 1, outside: 1})
        basement.add_exit(living_room, 0)
        outside.add_exit(foyer, 1)

        knife = Item("Knife", "Knife", kitchen)
        rolling_pin = Item("Rolling Pin", "Rolling Pin", kitchen)
        car_keys = Item("Car Keys", "Car Keys", living_room)
        magazine = Item("Magazine", "Magazine", living_room)
        spare_change = Item("Spare Change", "Spare Change", foyer)
        basement_key = Item("Basement Key", "Basement Key", foyer, required_location=living_room)
        survey_footage = Item("Surveillance Footage", "Surveillance Footage",
                              basement, evidence=True)
        garden_gnome = Item("Garden Gnome", "Garden Gnome", outside, False)
        spare_key = Item("Spare Key", "Spare Key", outside)

        kitchen.add_item(knife)
        kitchen.add_item(rolling_pin)
        living_room.add_item(car_keys)
        living_room.add_item(magazine)
        foyer.add_item(spare_change)
        foyer.add_item(basement_key)
        basement.add_item(survey_footage)
        outside.add_item(garden_gnome)
        outside.add_item(spare_key)

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

        self.__locations = [kitchen, living_room, foyer, basement, outside]

        player = Player(kitchen)
        ai = AiAgent({'move': 1, 'search': 2, 'talk': 2}, living_room, [survey_footage])

        return player, ai
