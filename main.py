#!/usr/bin/env python3
"""
Ouroboros - Ring of Eternity
A retro Atari 2600-style action-adventure game

Main entry point for the game.
"""

from src.core.game import Game


def main():
    """Main game entry point"""
    print("Ouroboros - Ring of Eternity")
    print("=" * 40)

    # Create and run the game
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
