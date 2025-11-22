"""
Camera system for screen transitions and viewport management
"""

import pygame
from src.core.constants import NATIVE_WIDTH, NATIVE_HEIGHT
from src.world.screen import Direction


class Camera:
    """
    Manages the viewport and screen transitions
    """

    def __init__(self):
        """Initialize the camera"""
        self.x = 0
        self.y = 0
        self.transitioning = False
        self.transition_direction = None
        self.transition_progress = 0
        self.transition_speed = 4  # pixels per frame

    def check_screen_transition(self, player_x: float, player_y: float,
                                 player_width: int, player_height: int) -> Direction:
        """
        Check if the player has moved off screen and needs to transition

        Args:
            player_x: Player X position
            player_y: Player Y position
            player_width: Player width
            player_height: Player height

        Returns:
            Direction to transition, or None
        """
        # Check if player has completely exited the screen
        if player_x + player_width < 0:
            return Direction.WEST
        elif player_x > NATIVE_WIDTH:
            return Direction.EAST
        elif player_y + player_height < 0:
            return Direction.NORTH
        elif player_y > NATIVE_HEIGHT:
            return Direction.SOUTH

        return None

    def start_transition(self, direction: Direction):
        """
        Start a screen transition

        Args:
            direction: Direction to transition
        """
        if not self.transitioning:
            self.transitioning = True
            self.transition_direction = direction
            self.transition_progress = 0

    def update_transition(self) -> bool:
        """
        Update transition animation

        Returns:
            True if transition is complete, False otherwise
        """
        if not self.transitioning:
            return True

        self.transition_progress += self.transition_speed

        # Simple instant transition for now
        # Can add smooth scrolling animation later
        if self.transition_progress >= NATIVE_WIDTH:
            self.transitioning = False
            self.transition_progress = 0
            return True

        return False

    def get_player_spawn_position(self, direction: Direction,
                                   player_width: int,
                                   player_height: int) -> tuple:
        """
        Get the player spawn position when entering from a direction

        Args:
            direction: Direction player came from
            player_width: Player width
            player_height: Player height

        Returns:
            (x, y) spawn position
        """
        margin = 8  # Margin from edge

        if direction == Direction.WEST:
            # Coming from west, spawn on east side
            return (NATIVE_WIDTH - player_width - margin,
                    NATIVE_HEIGHT // 2 - player_height // 2)
        elif direction == Direction.EAST:
            # Coming from east, spawn on west side
            return (margin, NATIVE_HEIGHT // 2 - player_height // 2)
        elif direction == Direction.NORTH:
            # Coming from north, spawn on south side
            return (NATIVE_WIDTH // 2 - player_width // 2,
                    NATIVE_HEIGHT - player_height - margin)
        elif direction == Direction.SOUTH:
            # Coming from south, spawn on north side
            return (NATIVE_WIDTH // 2 - player_width // 2, margin)

        return (NATIVE_WIDTH // 2, NATIVE_HEIGHT // 2)

    def get_opposite_direction(self, direction: Direction) -> Direction:
        """Get the opposite direction"""
        opposites = {
            Direction.NORTH: Direction.SOUTH,
            Direction.SOUTH: Direction.NORTH,
            Direction.EAST: Direction.WEST,
            Direction.WEST: Direction.EAST
        }
        return opposites.get(direction)
