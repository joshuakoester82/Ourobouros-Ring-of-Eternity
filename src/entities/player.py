"""
Player entity for Ouroboros - Ring of Eternity
"""

import pygame
from src.core.constants import (
    PLAYER_SIZE, PLAYER_SPEED,
    COLOR_WHITE, NATIVE_WIDTH, NATIVE_HEIGHT
)


class Player:
    """
    Player entity - 16x16 white square
    """

    def __init__(self, x: int, y: int):
        """
        Initialize the player

        Args:
            x: Starting x position
            y: Starting y position
        """
        self.x = x
        self.y = y
        self.width = PLAYER_SIZE
        self.height = PLAYER_SIZE
        self.speed = PLAYER_SPEED

        # Create player sprite (white square)
        self.sprite = pygame.Surface((self.width, self.height))
        self.sprite.fill(COLOR_WHITE)

        # Inventory (one-slot system)
        self.held_item = None

        # Movement state
        self.velocity_x = 0
        self.velocity_y = 0

    def handle_input(self):
        """
        Handle keyboard input for player movement
        Non-inertial movement (instant stop when key released)
        """
        keys = pygame.key.get_pressed()

        # Reset velocity
        self.velocity_x = 0
        self.velocity_y = 0

        # WASD and Arrow key controls
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velocity_x = -self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocity_x = self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.velocity_y = -self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.velocity_y = self.speed

    def update(self, current_screen=None):
        """
        Update player position

        Args:
            current_screen: Current screen for collision detection
        """
        # Store old position for collision recovery
        old_x = self.x
        old_y = self.y

        # Update position based on velocity
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Check collision with screen if provided
        if current_screen is not None:
            # Check all four corners of the player
            corners = [
                (self.x, self.y),  # Top-left
                (self.x + self.width - 1, self.y),  # Top-right
                (self.x, self.y + self.height - 1),  # Bottom-left
                (self.x + self.width - 1, self.y + self.height - 1)  # Bottom-right
            ]

            # If any corner collides with a solid tile, revert position
            for corner_x, corner_y in corners:
                if current_screen.is_tile_solid(corner_x, corner_y):
                    self.x = old_x
                    self.y = old_y
                    break

            # Check collision with solid interactable objects
            player_rect = pygame.Rect(self.x, self.y, self.width, self.height)
            for entity in current_screen.entities:
                if hasattr(entity, 'solid') and entity.solid and hasattr(entity, 'active') and entity.active:
                    entity_rect = entity.get_rect()
                    if player_rect.colliderect(entity_rect):
                        self.x = old_x
                        self.y = old_y
                        break

        # Keep player within screen boundaries (allow slightly off-screen for transitions)
        # Extended bounds to allow screen transitions
        self.x = max(-self.width, min(self.x, NATIVE_WIDTH))
        self.y = max(-self.height, min(self.y, NATIVE_HEIGHT))

    def render(self, surface: pygame.Surface):
        """
        Render the player to the given surface

        Args:
            surface: Surface to render to (should be native resolution)
        """
        surface.blit(self.sprite, (int(self.x), int(self.y)))

    def get_rect(self) -> pygame.Rect:
        """Get the player's bounding rectangle"""
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def pick_up_item(self, item):
        """
        Pick up an item (one-slot inventory)

        Args:
            item: The item to pick up

        Returns:
            bool: True if picked up, False if inventory full
        """
        if self.held_item is None:
            self.held_item = item
            return True
        return False

    def drop_item(self):
        """
        Drop the currently held item

        Returns:
            The dropped item, or None if not holding anything
        """
        item = self.held_item
        self.held_item = None
        return item

    def has_item(self) -> bool:
        """Check if player is holding an item"""
        return self.held_item is not None
