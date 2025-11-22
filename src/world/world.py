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
        self._add_room_layouts()

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

    def _add_room_layouts(self):
        """Add detailed wall layouts to each room for visual interest and challenge"""
        # Tower Hub - Four pillars in corners + central area
        hub = self.screens[ScreenID.TOWER_HUB]
        # Corner pillars (2x2 tiles each)
        for px, py in [(1, 1), (7, 1), (1, 9), (7, 9)]:
            hub.set_tile_solid(px, py, True)
            hub.set_tile_solid(px+1, py, True)
            hub.set_tile_solid(px, py+1, True)
            hub.set_tile_solid(px+1, py+1, True)

        # Gardens 1 - Entrance with side bushes
        g1 = self.screens[ScreenID.GARDENS_1]
        # Side obstacles
        for y in range(2, 5):
            g1.set_tile_solid(2, y, True)
            g1.set_tile_solid(7, y, True)

        # Gardens 2 - Open area with scattered obstacles
        g2 = self.screens[ScreenID.GARDENS_2]
        g2.set_tile_solid(3, 4, True)
        g2.set_tile_solid(6, 7, True)
        g2.set_tile_solid(4, 9, True)

        # Gardens 3 - Path with obstacles (chasm puzzle area)
        g3 = self.screens[ScreenID.GARDENS_3]
        # L-shaped wall
        for x in range(2, 5):
            g3.set_tile_solid(x, 3, True)
        for y in range(3, 7):
            g3.set_tile_solid(4, y, True)

        # Gardens 4 - Narrow passages leading to tree
        g4 = self.screens[ScreenID.GARDENS_4]
        for y in range(1, 6):
            g4.set_tile_solid(3, y, True)
        for y in range(7, 11):
            g4.set_tile_solid(6, y, True)

        # Catacombs 1 - Narrow entrance corridor
        c1 = self.screens[ScreenID.CATACOMBS_1]
        # Side walls creating corridor
        for y in range(1, 8):
            c1.set_tile_solid(3, y, True)
            c1.set_tile_solid(6, y, True)

        # Catacombs 2 - Chamber with pillars
        c2 = self.screens[ScreenID.CATACOMBS_2]
        c2.set_tile_solid(3, 4, True)
        c2.set_tile_solid(6, 4, True)
        c2.set_tile_solid(3, 8, True)
        c2.set_tile_solid(6, 8, True)

        # Catacombs 3 - Ogre's lair with alcoves
        c3 = self.screens[ScreenID.CATACOMBS_3]
        # Create alcoves
        for x in range(1, 3):
            c3.set_tile_solid(x, 4, True)
            c3.set_tile_solid(x, 8, True)
        for x in range(7, 9):
            c3.set_tile_solid(x, 4, True)
            c3.set_tile_solid(x, 8, True)

        # Catacombs 4 - Cracked wall room with obstacles
        c4 = self.screens[ScreenID.CATACOMBS_4]
        # Scattered rubble
        c4.set_tile_solid(2, 3, True)
        c4.set_tile_solid(7, 3, True)
        c4.set_tile_solid(2, 9, True)
        c4.set_tile_solid(7, 9, True)

        # Ruins 1 - Flooded entrance
        r1 = self.screens[ScreenID.RUINS_1]
        # Broken walls
        for x in range(2, 4):
            r1.set_tile_solid(x, 5, True)
        for x in range(6, 8):
            r1.set_tile_solid(x, 7, True)

        # Ruins 2 - Maze layout
        r2 = self.screens[ScreenID.RUINS_2]
        # Create maze walls
        for y in range(2, 7):
            r2.set_tile_solid(3, y, True)
        for x in range(5, 8):
            r2.set_tile_solid(x, 5, True)
        r2.set_tile_solid(5, 8, True)
        r2.set_tile_solid(5, 9, True)

        # Ruins 3 - Toxic basin room with careful paths
        r3 = self.screens[ScreenID.RUINS_3]
        # Narrow paths around basin
        for x in range(2, 4):
            r3.set_tile_solid(x, 3, True)
        for x in range(6, 8):
            r3.set_tile_solid(x, 3, True)

        # Ruins 4 - Blessed Spring chamber
        r4 = self.screens[ScreenID.RUINS_4]
        # Pool edges
        for x in range(4, 7):
            r4.set_tile_solid(x, 4, True)
            r4.set_tile_solid(x, 9, True)

        # Cliffs 1 - Windy entrance
        cl1 = self.screens[ScreenID.CLIFFS_1]
        # Scattered rocks
        cl1.set_tile_solid(2, 4, True)
        cl1.set_tile_solid(7, 6, True)
        cl1.set_tile_solid(4, 9, True)

        # Cliffs 2 - Flute chamber with platforms
        cl2 = self.screens[ScreenID.CLIFFS_2]
        # Platform-like obstacles
        for x in range(2, 4):
            cl2.set_tile_solid(x, 3, True)
        for x in range(6, 8):
            cl2.set_tile_solid(x, 8, True)

        # Cliffs 3 - Ascending platforms
        cl3 = self.screens[ScreenID.CLIFFS_3]
        # Step-like pattern
        cl3.set_tile_solid(2, 8, True)
        cl3.set_tile_solid(3, 6, True)
        cl3.set_tile_solid(5, 4, True)
        cl3.set_tile_solid(7, 2, True)

        # Cliffs 4 - Statue chamber
        cl4 = self.screens[ScreenID.CLIFFS_4]
        # Create a chamber feel
        for y in range(3, 6):
            cl4.set_tile_solid(2, y, True)
            cl4.set_tile_solid(7, y, True)

        # Final Chamber - Boss arena with corner pillars
        final = self.screens[ScreenID.FINAL_CHAMBER]
        # Just corner markers for dramatic effect
        final.set_tile_solid(2, 2, True)
        final.set_tile_solid(7, 2, True)
        final.set_tile_solid(2, 9, True)
        final.set_tile_solid(7, 9, True)

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
