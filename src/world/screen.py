"""
Screen/Room system for Ouroboros - Ring of Eternity
"""

import pygame
from enum import Enum, auto
from typing import Optional, Dict, List
from src.core.constants import NATIVE_WIDTH, NATIVE_HEIGHT, COLOR_GRAY, TILE_SIZE


class ScreenID(Enum):
    """Identifiers for each screen in the game"""
    # Hub
    TOWER_HUB = "tower_hub"

    # Final Chamber (behind Silver Gate)
    FINAL_CHAMBER = "final_chamber"

    # North - Withered Gardens (Earth)
    GARDENS_1 = "gardens_1"
    GARDENS_2 = "gardens_2"
    GARDENS_3 = "gardens_3"
    GARDENS_4 = "gardens_4"

    # East - Catacombs (Fire/Dark)
    CATACOMBS_1 = "catacombs_1"
    CATACOMBS_2 = "catacombs_2"
    CATACOMBS_3 = "catacombs_3"
    CATACOMBS_4 = "catacombs_4"

    # South - Sunken Ruins (Water)
    RUINS_1 = "ruins_1"
    RUINS_2 = "ruins_2"
    RUINS_3 = "ruins_3"
    RUINS_4 = "ruins_4"

    # West - High Cliffs (Air)
    CLIFFS_1 = "cliffs_1"
    CLIFFS_2 = "cliffs_2"
    CLIFFS_3 = "cliffs_3"
    CLIFFS_4 = "cliffs_4"


class Direction(Enum):
    """Cardinal directions for screen connections"""
    NORTH = auto()
    SOUTH = auto()
    EAST = auto()
    WEST = auto()


class Screen:
    """
    Represents a single screen/room in the game world
    """

    def __init__(self, screen_id: ScreenID, name: str, color: tuple = COLOR_GRAY):
        """
        Initialize a screen

        Args:
            screen_id: Unique identifier for this screen
            name: Display name for the screen
            color: Background color for the screen
        """
        self.id = screen_id
        self.name = name
        self.background_color = color

        # Screen connections (which screens are adjacent)
        self.connections: Dict[Direction, Optional[ScreenID]] = {
            Direction.NORTH: None,
            Direction.SOUTH: None,
            Direction.EAST: None,
            Direction.WEST: None
        }

        # Tiles for collision (16x16 grid)
        # True = solid wall, False = passable
        self.tiles: List[List[bool]] = []
        self._init_tiles()

        # Entities on this screen (enemies, items, etc.)
        self.entities = []

    def _init_tiles(self):
        """Initialize the tile grid"""
        rows = NATIVE_HEIGHT // TILE_SIZE  # 12 rows
        cols = NATIVE_WIDTH // TILE_SIZE   # 10 columns

        # Create empty grid (all passable)
        self.tiles = [[False for _ in range(cols)] for _ in range(rows)]

        # Add border walls by default
        for row in range(rows):
            self.tiles[row][0] = True  # Left wall
            self.tiles[row][cols - 1] = True  # Right wall

        for col in range(cols):
            self.tiles[0][col] = True  # Top wall
            self.tiles[rows - 1][col] = True  # Bottom wall

    def connect(self, direction: Direction, screen_id: ScreenID):
        """
        Connect this screen to another in a given direction

        Args:
            direction: Direction of the connection
            screen_id: ID of the connected screen
        """
        self.connections[direction] = screen_id

    def get_connection(self, direction: Direction) -> Optional[ScreenID]:
        """Get the screen connected in the given direction"""
        return self.connections[direction]

    def is_tile_solid(self, x: int, y: int) -> bool:
        """
        Check if a tile at pixel position is solid

        Args:
            x: X position in pixels
            y: Y position in pixels

        Returns:
            True if solid, False if passable
        """
        tile_x = int(x // TILE_SIZE)
        tile_y = int(y // TILE_SIZE)

        rows = len(self.tiles)
        cols = len(self.tiles[0]) if rows > 0 else 0

        if 0 <= tile_y < rows and 0 <= tile_x < cols:
            return self.tiles[tile_y][tile_x]

        return True  # Out of bounds = solid

    def set_tile_solid(self, tile_x: int, tile_y: int, solid: bool = True):
        """
        Set a tile to be solid or passable

        Args:
            tile_x: X coordinate in tile grid
            tile_y: Y coordinate in tile grid
            solid: True for solid, False for passable
        """
        rows = len(self.tiles)
        cols = len(self.tiles[0]) if rows > 0 else 0

        if 0 <= tile_y < rows and 0 <= tile_x < cols:
            self.tiles[tile_y][tile_x] = solid

    def render(self, surface: pygame.Surface):
        """
        Render the screen

        Args:
            surface: Surface to render to
        """
        # Fill background
        surface.fill(self.background_color)

        # Render tiles (for debugging, can be replaced with sprites later)
        for row_idx, row in enumerate(self.tiles):
            for col_idx, is_solid in enumerate(row):
                if is_solid:
                    x = col_idx * TILE_SIZE
                    y = row_idx * TILE_SIZE
                    pygame.draw.rect(
                        surface,
                        (100, 100, 100),  # Gray walls
                        (x, y, TILE_SIZE, TILE_SIZE)
                    )

        # Render entities
        for entity in self.entities:
            if hasattr(entity, 'render'):
                entity.render(surface)
