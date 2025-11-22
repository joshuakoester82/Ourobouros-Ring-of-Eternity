"""
World manager for Ouroboros - Ring of Eternity
"""

from typing import Dict
from src.world.screen import Screen, ScreenID, Direction
from src.core.constants import (
    COLOR_BLACK, COLOR_GREEN, COLOR_RED,
    COLOR_BLUE, COLOR_YELLOW, COLOR_GRAY
)


class World:
    """
    Manages all screens and world layout
    """

    def __init__(self):
        """Initialize the world"""
        self.screens: Dict[ScreenID, Screen] = {}
        self.current_screen_id = ScreenID.TOWER_HUB

        # Build the world
        self._create_screens()
        self._connect_screens()

    def _create_screens(self):
        """Create all 24 screens"""
        # Hub - Tower
        self.screens[ScreenID.TOWER_HUB] = Screen(
            ScreenID.TOWER_HUB,
            "The Ouroboros Tower",
            COLOR_GRAY
        )

        # North - Withered Gardens (Earth - Green tones)
        earth_color = (40, 50, 30)  # Dark greenish
        self.screens[ScreenID.GARDENS_1] = Screen(
            ScreenID.GARDENS_1,
            "Withered Gardens - Entrance",
            earth_color
        )
        self.screens[ScreenID.GARDENS_2] = Screen(
            ScreenID.GARDENS_2,
            "Withered Gardens - Acorn Grove",
            earth_color
        )
        self.screens[ScreenID.GARDENS_3] = Screen(
            ScreenID.GARDENS_3,
            "Withered Gardens - Soft Dirt",
            earth_color
        )
        self.screens[ScreenID.GARDENS_4] = Screen(
            ScreenID.GARDENS_4,
            "Withered Gardens - Hollow Tree",
            earth_color
        )

        # East - Catacombs (Fire/Dark - Red/black tones)
        fire_color = (40, 20, 20)  # Dark reddish
        self.screens[ScreenID.CATACOMBS_1] = Screen(
            ScreenID.CATACOMBS_1,
            "Catacombs - Gold Gate",
            fire_color
        )
        self.screens[ScreenID.CATACOMBS_2] = Screen(
            ScreenID.CATACOMBS_2,
            "Catacombs - Bomb Chamber",
            fire_color
        )
        self.screens[ScreenID.CATACOMBS_3] = Screen(
            ScreenID.CATACOMBS_3,
            "Catacombs - Ogre's Lair",
            fire_color
        )
        self.screens[ScreenID.CATACOMBS_4] = Screen(
            ScreenID.CATACOMBS_4,
            "Catacombs - Cracked Wall",
            fire_color
        )

        # South - Sunken Ruins (Water - Blue tones)
        water_color = (20, 30, 50)  # Dark bluish
        self.screens[ScreenID.RUINS_1] = Screen(
            ScreenID.RUINS_1,
            "Sunken Ruins - Entrance",
            water_color
        )
        self.screens[ScreenID.RUINS_2] = Screen(
            ScreenID.RUINS_2,
            "Sunken Ruins - Maze",
            water_color
        )
        self.screens[ScreenID.RUINS_3] = Screen(
            ScreenID.RUINS_3,
            "Sunken Ruins - Toxic Basin",
            water_color
        )
        self.screens[ScreenID.RUINS_4] = Screen(
            ScreenID.RUINS_4,
            "Sunken Ruins - Blessed Spring",
            water_color
        )

        # West - High Cliffs (Air - Light/yellow tones)
        air_color = (50, 50, 40)  # Grayish-yellow
        self.screens[ScreenID.CLIFFS_1] = Screen(
            ScreenID.CLIFFS_1,
            "High Cliffs - Sheet Music",
            air_color
        )
        self.screens[ScreenID.CLIFFS_2] = Screen(
            ScreenID.CLIFFS_2,
            "High Cliffs - Flute Chamber",
            air_color
        )
        self.screens[ScreenID.CLIFFS_3] = Screen(
            ScreenID.CLIFFS_3,
            "High Cliffs - Ascent",
            air_color
        )
        self.screens[ScreenID.CLIFFS_4] = Screen(
            ScreenID.CLIFFS_4,
            "High Cliffs - Sleepless Statue",
            air_color
        )

        # Final Chamber (behind Silver Gate) - Dark/mysterious
        final_color = (10, 10, 20)  # Very dark blue
        self.screens[ScreenID.FINAL_CHAMBER] = Screen(
            ScreenID.FINAL_CHAMBER,
            "The Final Chamber",
            final_color
        )

    def _connect_screens(self):
        """Set up connections between screens"""
        # Hub connections (center of the web)
        hub = self.screens[ScreenID.TOWER_HUB]
        hub.connect(Direction.NORTH, ScreenID.GARDENS_1)
        hub.connect(Direction.EAST, ScreenID.CATACOMBS_1)
        hub.connect(Direction.SOUTH, ScreenID.RUINS_1)
        hub.connect(Direction.WEST, ScreenID.CLIFFS_1)

        # North - Gardens chain
        self.screens[ScreenID.GARDENS_1].connect(Direction.SOUTH, ScreenID.TOWER_HUB)
        self.screens[ScreenID.GARDENS_1].connect(Direction.NORTH, ScreenID.GARDENS_2)

        self.screens[ScreenID.GARDENS_2].connect(Direction.SOUTH, ScreenID.GARDENS_1)
        self.screens[ScreenID.GARDENS_2].connect(Direction.WEST, ScreenID.GARDENS_3)

        self.screens[ScreenID.GARDENS_3].connect(Direction.EAST, ScreenID.GARDENS_2)
        self.screens[ScreenID.GARDENS_3].connect(Direction.NORTH, ScreenID.GARDENS_4)

        self.screens[ScreenID.GARDENS_4].connect(Direction.SOUTH, ScreenID.GARDENS_3)

        # East - Catacombs chain
        self.screens[ScreenID.CATACOMBS_1].connect(Direction.WEST, ScreenID.TOWER_HUB)
        self.screens[ScreenID.CATACOMBS_1].connect(Direction.EAST, ScreenID.CATACOMBS_2)

        self.screens[ScreenID.CATACOMBS_2].connect(Direction.WEST, ScreenID.CATACOMBS_1)
        self.screens[ScreenID.CATACOMBS_2].connect(Direction.NORTH, ScreenID.CATACOMBS_3)

        self.screens[ScreenID.CATACOMBS_3].connect(Direction.SOUTH, ScreenID.CATACOMBS_2)
        self.screens[ScreenID.CATACOMBS_3].connect(Direction.EAST, ScreenID.CATACOMBS_4)

        self.screens[ScreenID.CATACOMBS_4].connect(Direction.WEST, ScreenID.CATACOMBS_3)

        # South - Ruins chain
        self.screens[ScreenID.RUINS_1].connect(Direction.NORTH, ScreenID.TOWER_HUB)
        self.screens[ScreenID.RUINS_1].connect(Direction.SOUTH, ScreenID.RUINS_2)

        self.screens[ScreenID.RUINS_2].connect(Direction.NORTH, ScreenID.RUINS_1)
        self.screens[ScreenID.RUINS_2].connect(Direction.EAST, ScreenID.RUINS_3)

        self.screens[ScreenID.RUINS_3].connect(Direction.WEST, ScreenID.RUINS_2)
        self.screens[ScreenID.RUINS_3].connect(Direction.SOUTH, ScreenID.RUINS_4)

        self.screens[ScreenID.RUINS_4].connect(Direction.NORTH, ScreenID.RUINS_3)

        # West - Cliffs chain
        self.screens[ScreenID.CLIFFS_1].connect(Direction.EAST, ScreenID.TOWER_HUB)
        self.screens[ScreenID.CLIFFS_1].connect(Direction.WEST, ScreenID.CLIFFS_2)

        self.screens[ScreenID.CLIFFS_2].connect(Direction.EAST, ScreenID.CLIFFS_1)
        self.screens[ScreenID.CLIFFS_2].connect(Direction.SOUTH, ScreenID.CLIFFS_3)

        self.screens[ScreenID.CLIFFS_3].connect(Direction.NORTH, ScreenID.CLIFFS_2)
        self.screens[ScreenID.CLIFFS_3].connect(Direction.WEST, ScreenID.CLIFFS_4)

        self.screens[ScreenID.CLIFFS_4].connect(Direction.EAST, ScreenID.CLIFFS_3)

    def get_current_screen(self) -> Screen:
        """Get the current screen"""
        return self.screens[self.current_screen_id]

    def change_screen(self, direction: Direction) -> bool:
        """
        Attempt to change to an adjacent screen

        Args:
            direction: Direction to move

        Returns:
            True if screen changed, False if no connection
        """
        current = self.get_current_screen()
        next_screen_id = current.get_connection(direction)

        if next_screen_id is not None:
            self.current_screen_id = next_screen_id
            print(f"Moved to: {self.screens[next_screen_id].name}")
            return True

        return False

    def get_screen(self, screen_id: ScreenID) -> Screen:
        """Get a specific screen by ID"""
        return self.screens.get(screen_id)
