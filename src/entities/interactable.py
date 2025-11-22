"""
Interactable objects system for Ouroboros - Ring of Eternity
"""

import pygame
from enum import Enum, auto
from typing import Optional
from src.core.constants import COLOR_WHITE, COLOR_GREEN, COLOR_RED, COLOR_BLUE, COLOR_YELLOW, COLOR_GRAY


class InteractableType(Enum):
    """Types of interactable objects"""
    # Pedestals for crystals
    PEDESTAL_GREEN = auto()
    PEDESTAL_RED = auto()
    PEDESTAL_BLUE = auto()
    PEDESTAL_YELLOW = auto()

    # Gates
    GOLD_GATE = auto()
    SILVER_GATE = auto()

    # Puzzle elements
    FOUNTAIN = auto()
    SOFT_DIRT = auto()
    CRACKED_WALL = auto()
    TOXIC_BASIN = auto()
    BLESSED_SPRING = auto()
    SLEEPLESS_STATUE = auto()
    CHASM = auto()


class Interactable:
    """
    Base class for interactable objects in the game
    """

    def __init__(self, interactable_type: InteractableType, x: float, y: float,
                 width: int = 16, height: int = 16, color: tuple = COLOR_GRAY):
        """
        Initialize an interactable object

        Args:
            interactable_type: Type of the interactable
            x: X position in world
            y: Y position in world
            width: Width of the object
            height: Height of the object
            color: Color of the object
        """
        self.interactable_type = interactable_type
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.active = True
        self.solid = True  # Whether it blocks player movement

        # Interaction properties
        self.interaction_range = 24  # Pixels from player
        self.requires_item = None  # ItemType required to interact
        self.is_activated = False  # Whether it's been used/solved

        # Create basic sprite
        self.sprite = pygame.Surface((width, height))
        self.sprite.fill(color)

    def get_rect(self) -> pygame.Rect:
        """Get the object's bounding rectangle"""
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def is_near_player(self, player_x: float, player_y: float,
                       player_width: int, player_height: int) -> bool:
        """
        Check if object is within interaction range of player

        Args:
            player_x: Player X position
            player_y: Player Y position
            player_width: Player width
            player_height: Player height

        Returns:
            True if within range, False otherwise
        """
        # Calculate centers
        obj_center_x = self.x + self.width / 2
        obj_center_y = self.y + self.height / 2
        player_center_x = player_x + player_width / 2
        player_center_y = player_y + player_height / 2

        # Calculate distance
        dx = obj_center_x - player_center_x
        dy = obj_center_y - player_center_y
        distance = (dx * dx + dy * dy) ** 0.5

        return distance <= self.interaction_range

    def can_interact_with_item(self, item) -> bool:
        """
        Check if a specific item can be used with this interactable

        Args:
            item: Item to check

        Returns:
            True if item can be used, False otherwise
        """
        if self.is_activated:
            return False
        if self.requires_item is None:
            return False
        return hasattr(item, 'item_type') and item.item_type == self.requires_item

    def interact(self, item=None):
        """
        Handle interaction with this object
        Override in subclasses for specific behavior

        Args:
            item: Optional item being used

        Returns:
            Result of interaction (varies by type)
        """
        return None

    def render(self, surface: pygame.Surface):
        """
        Render the interactable object

        Args:
            surface: Surface to render to
        """
        if self.active:
            surface.blit(self.sprite, (int(self.x), int(self.y)))

    def get_name(self) -> str:
        """Get the display name of the object"""
        names = {
            InteractableType.PEDESTAL_GREEN: "Green Pedestal",
            InteractableType.PEDESTAL_RED: "Red Pedestal",
            InteractableType.PEDESTAL_BLUE: "Blue Pedestal",
            InteractableType.PEDESTAL_YELLOW: "Yellow Pedestal",
            InteractableType.GOLD_GATE: "Gold Gate",
            InteractableType.SILVER_GATE: "Silver Gate",
            InteractableType.FOUNTAIN: "Fountain",
            InteractableType.SOFT_DIRT: "Soft Dirt",
            InteractableType.CRACKED_WALL: "Cracked Wall",
            InteractableType.TOXIC_BASIN: "Toxic Basin",
            InteractableType.BLESSED_SPRING: "Blessed Spring",
            InteractableType.SLEEPLESS_STATUE: "Sleepless Statue",
            InteractableType.CHASM: "Chasm"
        }
        return names.get(self.interactable_type, "Unknown Object")


class Pedestal(Interactable):
    """Crystal pedestal in the Tower Hub"""

    def __init__(self, x: float, y: float, crystal_type, outline_color: tuple):
        """
        Create a pedestal for a specific crystal

        Args:
            x: X position
            y: Y position
            crystal_type: ItemType of the crystal this pedestal accepts
            outline_color: Color of the pedestal outline
        """
        super().__init__(InteractableType.PEDESTAL_GREEN, x, y, 16, 16, COLOR_GRAY)
        self.requires_item = crystal_type
        self.outline_color = outline_color
        self.has_crystal = False
        self.solid = False  # Pedestals don't block movement

        # Create pedestal sprite with colored outline
        self.sprite = pygame.Surface((16, 16))
        self.sprite.fill(COLOR_GRAY)
        pygame.draw.rect(self.sprite, outline_color, (0, 0, 16, 16), 2)

    def interact(self, item=None):
        """Place crystal on pedestal"""
        if not self.has_crystal and self.can_interact_with_item(item):
            self.has_crystal = True
            self.is_activated = True
            # Update sprite to show crystal
            self.sprite.fill(self.outline_color)
            return True
        return False


class Gate(Interactable):
    """Locked gate that requires a key"""

    def __init__(self, x: float, y: float, width: int, height: int,
                 gate_type: InteractableType, key_type, color: tuple):
        """
        Create a locked gate

        Args:
            x: X position
            y: Y position
            width: Gate width
            height: Gate height
            gate_type: Type of gate (GOLD_GATE or SILVER_GATE)
            key_type: ItemType of key required
            color: Gate color
        """
        super().__init__(gate_type, x, y, width, height, color)
        self.requires_item = key_type
        self.solid = True

        # Create gate sprite with keyhole
        self.sprite = pygame.Surface((width, height))
        self.sprite.fill(color)
        # Draw keyhole
        keyhole_x = width // 2 - 2
        keyhole_y = height // 2 - 2
        pygame.draw.rect(self.sprite, COLOR_GRAY, (keyhole_x, keyhole_y, 4, 4))

    def interact(self, item=None):
        """Unlock gate with key"""
        if not self.is_activated and self.can_interact_with_item(item):
            self.is_activated = True
            self.solid = False
            self.active = False  # Gate disappears
            return True
        return False


class Fountain(Interactable):
    """Fountain for filling watering can"""

    def __init__(self, x: float, y: float):
        super().__init__(InteractableType.FOUNTAIN, x, y, 16, 16, COLOR_BLUE)
        self.solid = True
        from src.entities.item import ItemType
        self.requires_item = ItemType.WATERING_CAN

    def interact(self, item=None):
        """Fill watering can"""
        from src.entities.item import ItemType
        if item and hasattr(item, 'item_type'):
            if item.item_type == ItemType.WATERING_CAN:
                # Transform to filled watering can
                item.item_type = ItemType.WATERING_CAN_FULL
                item.color = COLOR_BLUE
                item.sprite.fill(COLOR_BLUE)
                return "filled"
        return None


class SoftDirt(Interactable):
    """Soft dirt patch where acorn can be planted"""

    def __init__(self, x: float, y: float):
        super().__init__(InteractableType.SOFT_DIRT, x, y, 16, 16, (101, 67, 33))
        self.solid = False
        self.has_acorn = False
        from src.entities.item import ItemType
        self.requires_item = ItemType.ACORN

    def interact(self, item=None):
        """Plant acorn or water it"""
        from src.entities.item import ItemType
        if not self.has_acorn and item and hasattr(item, 'item_type'):
            if item.item_type == ItemType.ACORN:
                self.has_acorn = True
                # Change color to show planted acorn
                self.sprite.fill((80, 50, 20))
                return "planted"
        elif self.has_acorn and item and hasattr(item, 'item_type'):
            if item.item_type == ItemType.WATERING_CAN_FULL:
                # Grow tree bridge
                return "grow_tree"
        return None


class CrackedWall(Interactable):
    """Cracked wall that can be destroyed with bomb"""

    def __init__(self, x: float, y: float):
        super().__init__(InteractableType.CRACKED_WALL, x, y, 16, 16, COLOR_GRAY)
        self.solid = True
        from src.entities.item import ItemType
        self.requires_item = ItemType.BOMB

        # Draw cracks
        self.sprite.fill(COLOR_GRAY)
        pygame.draw.line(self.sprite, (50, 50, 50), (2, 2), (14, 14), 1)
        pygame.draw.line(self.sprite, (50, 50, 50), (14, 2), (2, 14), 1)

    def interact(self, item=None):
        """Place bomb at wall"""
        from src.entities.item import ItemType
        if not self.is_activated and item and hasattr(item, 'item_type'):
            if item.item_type == ItemType.BOMB:
                return "bomb_placed"
        return None


class ToxicBasin(Interactable):
    """Toxic basin that kills on contact (until cleansed)"""

    def __init__(self, x: float, y: float, width: int = 32, height: int = 32):
        super().__init__(InteractableType.TOXIC_BASIN, x, y, width, height, (128, 0, 128))
        self.solid = False  # Can walk through but deadly
        self.deadly = True
        from src.entities.item import ItemType
        self.requires_item = ItemType.CHALICE_FILLED

    def interact(self, item=None):
        """Cleanse basin with filled chalice"""
        from src.entities.item import ItemType
        if not self.is_activated and item and hasattr(item, 'item_type'):
            if item.item_type == ItemType.CHALICE_FILLED:
                self.is_activated = True
                self.deadly = False
                self.active = False  # Basin disappears
                return "cleansed"
        return None


class BlessedSpring(Interactable):
    """Blessed spring for filling chalice"""

    def __init__(self, x: float, y: float):
        super().__init__(InteractableType.BLESSED_SPRING, x, y, 16, 16, (100, 200, 255))
        self.solid = True
        from src.entities.item import ItemType
        self.requires_item = ItemType.CHALICE

    def interact(self, item=None):
        """Fill chalice"""
        from src.entities.item import ItemType
        if item and hasattr(item, 'item_type'):
            if item.item_type == ItemType.CHALICE:
                # Transform to filled chalice
                item.item_type = ItemType.CHALICE_FILLED
                item.color = COLOR_BLUE
                item.sprite.fill(COLOR_BLUE)
                return "filled"
        return None


class SleeplessStatue(Interactable):
    """Statue that attacks player unless put to sleep with flute"""

    def __init__(self, x: float, y: float):
        super().__init__(InteractableType.SLEEPLESS_STATUE, x, y, 16, 24, COLOR_YELLOW)
        self.solid = True
        self.attack_range = 40
        from src.entities.item import ItemType
        self.requires_item = ItemType.FLUTE

        # Draw statue with eyes
        self.sprite.fill(COLOR_YELLOW)
        pygame.draw.rect(self.sprite, COLOR_RED, (4, 6, 3, 3))  # Left eye
        pygame.draw.rect(self.sprite, COLOR_RED, (9, 6, 3, 3))  # Right eye

    def interact(self, item=None):
        """Put statue to sleep with flute"""
        from src.entities.item import ItemType
        if not self.is_activated and item and hasattr(item, 'item_type'):
            if item.item_type == ItemType.FLUTE:
                self.is_activated = True
                # Draw closed eyes
                self.sprite.fill(COLOR_YELLOW)
                pygame.draw.line(self.sprite, COLOR_GRAY, (4, 7), (6, 7), 1)
                pygame.draw.line(self.sprite, COLOR_GRAY, (9, 7), (11, 7), 1)
                return "sleeping"
        return None


class Chasm(Interactable):
    """Wide chasm that blocks passage (until tree bridge is grown)"""

    def __init__(self, x: float, y: float, width: int = 16, height: int = 48):
        super().__init__(InteractableType.CHASM, x, y, width, height, (20, 20, 20))
        self.solid = True

    def grow_bridge(self):
        """Grow tree bridge to cross chasm"""
        self.solid = False
        self.sprite.fill((101, 67, 33))  # Brown tree bridge
