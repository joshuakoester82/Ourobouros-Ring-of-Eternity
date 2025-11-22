"""
Item system for Ouroboros - Ring of Eternity
"""

import pygame
from enum import Enum, auto
from src.core.constants import COLOR_WHITE


class ItemType(Enum):
    """Types of items in the game"""
    # Keys
    GOLD_KEY = auto()
    SILVER_KEY = auto()

    # Crystals
    GREEN_CRYSTAL = auto()  # Earth
    RED_CRYSTAL = auto()    # Fire
    BLUE_CRYSTAL = auto()   # Water
    YELLOW_CRYSTAL = auto() # Air

    # Puzzle items
    ACORN = auto()
    WATERING_CAN = auto()
    WATERING_CAN_FULL = auto()
    BOMB = auto()
    CHALICE = auto()
    CHALICE_FILLED = auto()
    FLUTE = auto()
    SWORD = auto()
    FISH = auto()  # Easter egg

    # Victory item
    RING_OF_ETERNITY = auto()


class Item:
    """
    Base class for all items in the game
    """

    def __init__(self, item_type: ItemType, x: float, y: float,
                 color: tuple = COLOR_WHITE, size: int = 8):
        """
        Initialize an item

        Args:
            item_type: Type of the item
            x: X position in world
            y: Y position in world
            color: Color of the item sprite
            size: Size of the item (square)
        """
        self.item_type = item_type
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.active = True  # Whether item is in the world or held

        # Create simple square sprite (can be enhanced later)
        self.sprite = pygame.Surface((size, size))
        self.sprite.fill(color)

        # Interaction properties
        self.pickup_range = 20  # Pixels from player center

    def get_rect(self) -> pygame.Rect:
        """Get the item's bounding rectangle"""
        return pygame.Rect(self.x, self.y, self.size, self.size)

    def is_near_player(self, player_x: float, player_y: float,
                       player_width: int, player_height: int) -> bool:
        """
        Check if item is within pickup range of player

        Args:
            player_x: Player X position
            player_y: Player Y position
            player_width: Player width
            player_height: Player height

        Returns:
            True if within range, False otherwise
        """
        # Calculate centers
        item_center_x = self.x + self.size / 2
        item_center_y = self.y + self.size / 2
        player_center_x = player_x + player_width / 2
        player_center_y = player_y + player_height / 2

        # Calculate distance
        dx = item_center_x - player_center_x
        dy = item_center_y - player_center_y
        distance = (dx * dx + dy * dy) ** 0.5

        return distance <= self.pickup_range

    def render(self, surface: pygame.Surface):
        """
        Render the item

        Args:
            surface: Surface to render to
        """
        if self.active:
            surface.blit(self.sprite, (int(self.x), int(self.y)))

            # Draw white outline when in pickup range (done by game logic)

    def get_name(self) -> str:
        """Get the display name of the item"""
        names = {
            ItemType.GOLD_KEY: "Gold Key",
            ItemType.SILVER_KEY: "Silver Key",
            ItemType.GREEN_CRYSTAL: "Green Crystal",
            ItemType.RED_CRYSTAL: "Red Crystal",
            ItemType.BLUE_CRYSTAL: "Blue Crystal",
            ItemType.YELLOW_CRYSTAL: "Yellow Crystal",
            ItemType.ACORN: "Acorn",
            ItemType.WATERING_CAN: "Watering Can",
            ItemType.WATERING_CAN_FULL: "Watering Can (Full)",
            ItemType.BOMB: "Bomb",
            ItemType.CHALICE: "Chalice",
            ItemType.CHALICE_FILLED: "Chalice (Filled)",
            ItemType.FLUTE: "Flute",
            ItemType.SWORD: "Sword",
            ItemType.FISH: "Fish",
            ItemType.RING_OF_ETERNITY: "Ring of Eternity"
        }
        return names.get(self.item_type, "Unknown Item")


def create_item(item_type: ItemType, x: float, y: float) -> Item:
    """
    Factory function to create items with appropriate colors

    Args:
        item_type: Type of item to create
        x: X position
        y: Y position

    Returns:
        Item instance
    """
    from src.core.constants import (
        COLOR_YELLOW, COLOR_GRAY, COLOR_GREEN, COLOR_RED,
        COLOR_BLUE, COLOR_ORANGE, COLOR_PURPLE, COLOR_WHITE
    )

    # Define colors for each item type
    colors = {
        ItemType.GOLD_KEY: COLOR_YELLOW,
        ItemType.SILVER_KEY: COLOR_GRAY,
        ItemType.GREEN_CRYSTAL: COLOR_GREEN,
        ItemType.RED_CRYSTAL: COLOR_RED,
        ItemType.BLUE_CRYSTAL: COLOR_BLUE,
        ItemType.YELLOW_CRYSTAL: COLOR_YELLOW,
        ItemType.ACORN: (101, 67, 33),  # Brown
        ItemType.WATERING_CAN: COLOR_GRAY,
        ItemType.WATERING_CAN_FULL: COLOR_BLUE,
        ItemType.BOMB: COLOR_RED,
        ItemType.CHALICE: COLOR_YELLOW,
        ItemType.CHALICE_FILLED: COLOR_BLUE,
        ItemType.FLUTE: (210, 180, 140),  # Tan
        ItemType.SWORD: COLOR_GRAY,
        ItemType.FISH: COLOR_ORANGE,
        ItemType.RING_OF_ETERNITY: COLOR_YELLOW  # Golden circle
    }

    color = colors.get(item_type, COLOR_WHITE)
    size = 12 if item_type == ItemType.RING_OF_ETERNITY else 8

    # Create the item
    item = Item(item_type, x, y, color, size)

    # Special sprite for Ring of Eternity (golden circle)
    if item_type == ItemType.RING_OF_ETERNITY:
        item.sprite = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(item.sprite, COLOR_YELLOW, (size // 2, size // 2), size // 2, 2)

    return item
