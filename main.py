"""Entry point for the game.

This module initializes the Game object and begins the game loop.
It is intended to be run as a script.
"""
from game import Game


def main():
    """Initializes the Game object and triggers the game to start its main loop."""
    game = Game()
    game.start_game()


if __name__ == "__main__":
    main()
