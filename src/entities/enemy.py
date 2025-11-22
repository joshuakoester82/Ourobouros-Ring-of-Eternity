"""
Enemy AI system for Ouroboros - Ring of Eternity
"""

import pygame
import random
import math
from enum import Enum, auto
from typing import List, Tuple, Optional
from src.core.constants import (
    COLOR_GREEN, COLOR_RED, COLOR_YELLOW,
    NATIVE_WIDTH, NATIVE_HEIGHT
)


class EnemyType(Enum):
    """Types of enemies"""
    CRAWLER = auto()  # Tier 1: Random movement
    CHASER = auto()   # Tier 2: Chases player
    SENTINEL = auto() # Tier 3: Patrols fixed route


class Enemy:
    """
    Base class for all enemies
    """

    def __init__(self, enemy_type: EnemyType, x: float, y: float,
                 size: int = 16, color: tuple = COLOR_GREEN, speed: float = 1.0):
        """
        Initialize an enemy

        Args:
            enemy_type: Type of enemy
            x: Starting X position
            y: Starting Y position
            size: Size of the enemy sprite
            color: Color of the enemy
            speed: Movement speed
        """
        self.enemy_type = enemy_type
        self.x = x
        self.y = y
        self.spawn_x = x  # Original spawn point
        self.spawn_y = y
        self.size = size
        self.color = color
        self.speed = speed
        self.active = True
        self.alive = True

        # Create simple sprite
        self.sprite = pygame.Surface((size, size))
        self.sprite.fill(color)

    def get_rect(self) -> pygame.Rect:
        """Get the enemy's bounding rectangle"""
        return pygame.Rect(self.x, self.y, self.size, self.size)

    def is_colliding_with_player(self, player_x: float, player_y: float,
                                  player_width: int, player_height: int) -> bool:
        """
        Check if enemy is colliding with player

        Args:
            player_x: Player X position
            player_y: Player Y position
            player_width: Player width
            player_height: Player height

        Returns:
            True if colliding, False otherwise
        """
        enemy_rect = self.get_rect()
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        return enemy_rect.colliderect(player_rect)

    def respawn(self):
        """Respawn enemy at original spawn point"""
        self.x = self.spawn_x
        self.y = self.spawn_y
        self.alive = True

    def update(self, player_x: float, player_y: float, current_screen=None):
        """
        Update enemy logic - override in subclasses

        Args:
            player_x: Player X position
            player_y: Player Y position
            current_screen: Current screen for collision detection
        """
        pass

    def render(self, surface: pygame.Surface):
        """
        Render the enemy

        Args:
            surface: Surface to render to
        """
        if self.active and self.alive:
            surface.blit(self.sprite, (int(self.x), int(self.y)))


class Crawler(Enemy):
    """
    Tier 1 Enemy: Green blob with random Brownian motion
    """

    def __init__(self, x: float, y: float):
        super().__init__(EnemyType.CRAWLER, x, y, 16, COLOR_GREEN, 0.5)

        # Movement state
        self.direction_x = 0
        self.direction_y = 0
        self.move_timer = 0
        self.pause_timer = 0
        self.is_paused = False

    def update(self, player_x: float, player_y: float, current_screen=None):
        """Update Crawler AI - random movement with pauses"""
        if not self.alive:
            return

        # Handle pause state
        if self.is_paused:
            self.pause_timer -= 1
            if self.pause_timer <= 0:
                self.is_paused = False
                self.move_timer = random.randint(60, 120)  # Move for 1-2 seconds
                # Choose new random direction (cardinal only)
                direction = random.choice(['north', 'south', 'east', 'west'])
                self.direction_x = 0
                self.direction_y = 0
                if direction == 'north':
                    self.direction_y = -1
                elif direction == 'south':
                    self.direction_y = 1
                elif direction == 'east':
                    self.direction_x = 1
                elif direction == 'west':
                    self.direction_x = -1
            return

        # Handle movement state
        self.move_timer -= 1
        if self.move_timer <= 0:
            self.is_paused = True
            self.pause_timer = random.randint(30, 60)  # Pause for 0.5-1 seconds
            return

        # Store old position for collision recovery
        old_x = self.x
        old_y = self.y

        # Move in current direction
        self.x += self.direction_x * self.speed
        self.y += self.direction_y * self.speed

        # Check wall collisions - bounce off walls
        if current_screen:
            # Check if hit a wall
            corners = [
                (self.x, self.y),
                (self.x + self.size - 1, self.y),
                (self.x, self.y + self.size - 1),
                (self.x + self.size - 1, self.y + self.size - 1)
            ]

            hit_wall = False
            for corner_x, corner_y in corners:
                if current_screen.is_tile_solid(corner_x, corner_y):
                    hit_wall = True
                    break

            if hit_wall:
                # Revert position and reverse direction
                self.x = old_x
                self.y = old_y
                self.direction_x = -self.direction_x
                self.direction_y = -self.direction_y

        # Keep within screen bounds
        if self.x < 16 or self.x > NATIVE_WIDTH - self.size - 16:
            self.x = old_x
            self.direction_x = -self.direction_x
        if self.y < 16 or self.y > NATIVE_HEIGHT - self.size - 16:
            self.y = old_y
            self.direction_y = -self.direction_y


class Chaser(Enemy):
    """
    Tier 2 Enemy: Red chevron/triangle that chases player using line-of-sight
    """

    def __init__(self, x: float, y: float):
        super().__init__(EnemyType.CHASER, x, y, 16, COLOR_RED, 1.5)

        # Create triangle sprite
        self.sprite = pygame.Surface((16, 16), pygame.SRCALPHA)
        points = [(8, 2), (14, 14), (2, 14)]  # Upward pointing triangle
        pygame.draw.polygon(self.sprite, COLOR_RED, points)

        # AI state
        self.aggro_range = 150  # Pixels
        self.is_chasing = False
        self.return_timer = 0

    def has_line_of_sight(self, player_x: float, player_y: float, current_screen) -> bool:
        """
        Check if enemy has clear line of sight to player

        Args:
            player_x: Player X position
            player_y: Player Y position
            current_screen: Current screen for raycasting

        Returns:
            True if line of sight is clear
        """
        # Calculate distance to player
        dx = player_x - self.x
        dy = player_y - self.y
        distance = math.sqrt(dx * dx + dy * dy)

        if distance > self.aggro_range:
            return False

        # Simple raycasting - check a few points along the line
        steps = int(distance / 8)  # Check every 8 pixels
        if steps == 0:
            return True

        for i in range(1, steps):
            t = i / steps
            check_x = self.x + dx * t
            check_y = self.y + dy * t
            if current_screen and current_screen.is_tile_solid(check_x, check_y):
                return False

        return True

    def update(self, player_x: float, player_y: float, current_screen=None):
        """Update Chaser AI - chase player if in line of sight"""
        if not self.alive:
            return

        # Check line of sight
        if current_screen and self.has_line_of_sight(player_x, player_y, current_screen):
            self.is_chasing = True
            self.return_timer = 180  # 3 seconds to return if player lost
        else:
            if self.is_chasing:
                self.return_timer -= 1
                if self.return_timer <= 0:
                    self.is_chasing = False

        if self.is_chasing:
            # Chase player at 75% of player speed (roughly)
            dx = player_x - self.x
            dy = player_y - self.y
            distance = math.sqrt(dx * dx + dy * dy)

            if distance > 0:
                # Normalize and apply speed
                move_x = (dx / distance) * self.speed
                move_y = (dy / distance) * self.speed

                # Store old position
                old_x = self.x
                old_y = self.y

                # Move
                self.x += move_x
                self.y += move_y

                # Check collisions
                if current_screen:
                    corners = [
                        (self.x, self.y),
                        (self.x + self.size - 1, self.y),
                        (self.x, self.y + self.size - 1),
                        (self.x + self.size - 1, self.y + self.size - 1)
                    ]

                    for corner_x, corner_y in corners:
                        if current_screen.is_tile_solid(corner_x, corner_y):
                            self.x = old_x
                            self.y = old_y
                            break
        else:
            # Return to spawn point
            dx = self.spawn_x - self.x
            dy = self.spawn_y - self.y
            distance = math.sqrt(dx * dx + dy * dy)

            if distance > 2:  # If not at spawn yet
                move_x = (dx / distance) * self.speed * 0.5
                move_y = (dy / distance) * self.speed * 0.5
                self.x += move_x
                self.y += move_y


class Sentinel(Enemy):
    """
    Tier 3 Enemy: Yellow serpentine shape that patrols a fixed route
    Immune to sword - must be avoided or distracted
    """

    def __init__(self, x: float, y: float, waypoints: List[Tuple[float, float]]):
        super().__init__(EnemyType.SENTINEL, x, y, 16, COLOR_YELLOW, 2.0)

        # Create serpentine sprite
        self.sprite = pygame.Surface((16, 16))
        self.sprite.fill(COLOR_YELLOW)
        pygame.draw.rect(self.sprite, (200, 200, 0), (4, 4, 8, 8))

        # Patrol route
        self.waypoints = waypoints if waypoints else [(x, y)]
        self.current_waypoint = 0
        self.immune_to_sword = True

    def update(self, player_x: float, player_y: float, current_screen=None):
        """Update Sentinel AI - patrol fixed route"""
        if not self.alive:
            return

        if not self.waypoints:
            return

        # Get current target waypoint
        target_x, target_y = self.waypoints[self.current_waypoint]

        # Calculate direction to waypoint
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx * dx + dy * dy)

        # If reached waypoint, move to next
        if distance < 5:
            self.current_waypoint = (self.current_waypoint + 1) % len(self.waypoints)
            return

        # Move towards waypoint
        if distance > 0:
            move_x = (dx / distance) * self.speed
            move_y = (dy / distance) * self.speed
            self.x += move_x
            self.y += move_y


def create_enemy(enemy_type: EnemyType, x: float, y: float,
                 waypoints: Optional[List[Tuple[float, float]]] = None) -> Enemy:
    """
    Factory function to create enemies

    Args:
        enemy_type: Type of enemy to create
        x: X position
        y: Y position
        waypoints: Optional waypoints for Sentinel

    Returns:
        Enemy instance
    """
    if enemy_type == EnemyType.CRAWLER:
        return Crawler(x, y)
    elif enemy_type == EnemyType.CHASER:
        return Chaser(x, y)
    elif enemy_type == EnemyType.SENTINEL:
        return Sentinel(x, y, waypoints or [])
    else:
        return Enemy(enemy_type, x, y)
