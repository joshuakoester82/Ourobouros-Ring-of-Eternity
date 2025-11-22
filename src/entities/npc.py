"""
NPC (Non-Player Character) classes for Ouroboros - Ring of Eternity

NPCs are static or semi-mobile entities that provide hints, companionship,
or other interactive features.
"""

import pygame
from enum import Enum, auto
from src.core.constants import (
    COLOR_BROWN, COLOR_ORANGE, COLOR_WHITE, COLOR_BLACK,
    NATIVE_WIDTH, NATIVE_HEIGHT
)


class NPCType(Enum):
    """Types of NPCs in the game"""
    OWL = auto()
    CAT = auto()


class NPC:
    """
    Base NPC class

    Args:
        x: X position
        y: Y position
        width: Sprite width
        height: Sprite height
        color: Sprite color
    """

    def __init__(self, x, y, width=16, height=16, color=COLOR_WHITE):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.active = True

        # Create sprite
        self.sprite = pygame.Surface((width, height))
        self.sprite.fill(color)

        # NPC type
        self.npc_type = None

    def update(self, player_x, player_y, player_held_item):
        """
        Update NPC logic

        Args:
            player_x: Player's x position
            player_y: Player's y position
            player_held_item: Item currently held by player (or None)
        """
        pass

    def render(self, surface):
        """
        Render the NPC

        Args:
            surface: Surface to render to
        """
        if self.active:
            surface.blit(self.sprite, (self.x, self.y))

    def is_near_player(self, player_x, player_y, player_width, player_height, distance=32):
        """
        Check if player is near this NPC

        Args:
            player_x: Player's x position
            player_y: Player's y position
            player_width: Player width
            player_height: Player height
            distance: Proximity distance threshold

        Returns:
            True if player is within distance
        """
        player_center_x = player_x + player_width // 2
        player_center_y = player_y + player_height // 2
        npc_center_x = self.x + self.width // 2
        npc_center_y = self.y + self.height // 2

        dx = player_center_x - npc_center_x
        dy = player_center_y - npc_center_y
        dist = (dx * dx + dy * dy) ** 0.5

        return dist < distance


class Owl(NPC):
    """
    The Owl NPC - perched in the North Biome

    If player approaches with the Flute, displays a hint about the "Song of Sleep"

    Args:
        x: X position
        y: Y position
    """

    def __init__(self, x, y):
        # Brown/orange owl sprite (16x16)
        super().__init__(x, y, width=16, height=16, color=COLOR_BROWN)

        self.npc_type = NPCType.OWL
        self.show_hint = False
        self.hint_timer = 0

        # Create a simple owl sprite
        self._create_owl_sprite()

    def _create_owl_sprite(self):
        """Create a simple pixelated owl sprite"""
        self.sprite.fill(COLOR_BLACK)  # Start with black background

        # Draw owl body (brown)
        pygame.draw.rect(self.sprite, COLOR_BROWN, (4, 6, 8, 8))

        # Draw owl head (brown)
        pygame.draw.rect(self.sprite, COLOR_BROWN, (3, 2, 10, 6))

        # Draw eyes (white)
        pygame.draw.rect(self.sprite, COLOR_WHITE, (5, 3, 2, 2))
        pygame.draw.rect(self.sprite, COLOR_WHITE, (9, 3, 2, 2))

        # Draw ear tufts (brown)
        pygame.draw.rect(self.sprite, COLOR_BROWN, (2, 1, 2, 2))
        pygame.draw.rect(self.sprite, COLOR_BROWN, (12, 1, 2, 2))

        # Draw beak (orange)
        pygame.draw.rect(self.sprite, COLOR_ORANGE, (7, 5, 2, 2))

    def update(self, player_x, player_y, player_held_item):
        """
        Update owl logic - check if player has flute nearby

        Args:
            player_x: Player's x position
            player_y: Player's y position
            player_held_item: Item currently held by player
        """
        # Check if player is near with flute
        if self.is_near_player(player_x, player_y, 16, 16, distance=40):
            # Check if player is holding the flute
            if player_held_item and hasattr(player_held_item, 'item_type'):
                from src.entities.item import ItemType
                if player_held_item.item_type == ItemType.FLUTE:
                    self.show_hint = True
                    self.hint_timer = 120  # Show for 2 seconds (60 FPS)
                else:
                    if self.hint_timer <= 0:
                        self.show_hint = False
        else:
            if self.hint_timer <= 0:
                self.show_hint = False

        # Countdown hint timer
        if self.hint_timer > 0:
            self.hint_timer -= 1

    def render(self, surface):
        """
        Render the owl and any hint text

        Args:
            surface: Surface to render to
        """
        super().render(surface)

        # Render hint text if active
        if self.show_hint and self.hint_timer > 0:
            pygame.font.init()
            font = pygame.font.Font(None, 12)
            hint_text = font.render("Song of Sleep...", True, COLOR_WHITE)

            # Position text above owl
            text_x = self.x + self.width // 2 - hint_text.get_width() // 2
            text_y = self.y - 15

            # Draw background box
            box_padding = 2
            box_rect = pygame.Rect(
                text_x - box_padding,
                text_y - box_padding,
                hint_text.get_width() + box_padding * 2,
                hint_text.get_height() + box_padding * 2
            )
            pygame.draw.rect(surface, COLOR_BLACK, box_rect)
            pygame.draw.rect(surface, COLOR_WHITE, box_rect, 1)

            # Draw text
            surface.blit(hint_text, (text_x, text_y))


class Cat(NPC):
    """
    The Cat NPC - spawns in Tower Hub

    If player drops Fish nearby, Cat will follow the player from screen to screen

    Args:
        x: X position
        y: Y position
    """

    def __init__(self, x, y):
        # Orange cat sprite (12x12, smaller than player)
        super().__init__(x, y, width=12, height=12, color=COLOR_ORANGE)

        self.npc_type = NPCType.CAT
        self.following = False
        self.target_x = x
        self.target_y = y
        self.speed = 1.5

        # Create a simple cat sprite
        self._create_cat_sprite()

    def _create_cat_sprite(self):
        """Create a simple pixelated cat sprite"""
        self.sprite.fill(COLOR_BLACK)  # Start with black background

        # Draw cat body (orange)
        pygame.draw.rect(self.sprite, COLOR_ORANGE, (2, 4, 8, 6))

        # Draw cat head (orange)
        pygame.draw.rect(self.sprite, COLOR_ORANGE, (3, 1, 6, 5))

        # Draw ears (orange)
        pygame.draw.rect(self.sprite, COLOR_ORANGE, (2, 0, 2, 2))
        pygame.draw.rect(self.sprite, COLOR_ORANGE, (8, 0, 2, 2))

        # Draw eyes (white)
        self.sprite.set_at((4, 2), COLOR_WHITE)
        self.sprite.set_at((7, 2), COLOR_WHITE)

        # Draw tail (orange)
        pygame.draw.rect(self.sprite, COLOR_ORANGE, (9, 6, 2, 4))

    def activate_following(self):
        """Activate the cat's following behavior"""
        self.following = True
        print("The cat begins to follow you!")

    def update(self, player_x, player_y, player_held_item):
        """
        Update cat logic - follow player if activated

        Args:
            player_x: Player's x position
            player_y: Player's y position
            player_held_item: Item currently held by player
        """
        if self.following:
            # Follow player with some lag
            self.target_x = player_x
            self.target_y = player_y

            # Move towards target
            dx = self.target_x - self.x
            dy = self.target_y - self.y
            distance = (dx * dx + dy * dy) ** 0.5

            # Only move if far enough away
            if distance > 20:
                if distance > 0:
                    # Normalize and apply speed
                    dx = (dx / distance) * self.speed
                    dy = (dy / distance) * self.speed

                    self.x += dx
                    self.y += dy

            # Keep cat on screen
            self.x = max(0, min(NATIVE_WIDTH - self.width, self.x))
            self.y = max(0, min(NATIVE_HEIGHT - self.height, self.y))

    def set_position(self, x, y):
        """
        Teleport cat to a position (used for screen transitions)

        Args:
            x: New x position
            y: New y position
        """
        self.x = x
        self.y = y


def create_npc(npc_type, x, y):
    """
    Factory function to create NPCs

    Args:
        npc_type: NPCType enum value
        x: X position
        y: Y position

    Returns:
        NPC instance
    """
    if npc_type == NPCType.OWL:
        return Owl(x, y)
    elif npc_type == NPCType.CAT:
        return Cat(x, y)
    else:
        raise ValueError(f"Unknown NPC type: {npc_type}")
